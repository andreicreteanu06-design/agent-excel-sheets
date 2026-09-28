import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import statsmodels.api as sm
import argparse
import sys
import re
import subprocess
import os

try:
    from google import genai
except ImportError:
    pass # Tratata mai jos in CLI

# ECONOMETRICS COPILOT - TERMINAL INTERACTIV (GEMINI API FREE-TIER)

# In loc sa punem cheia in cod (periculos pt GitHub), o citim din api_key.txt
def get_gemini_key():
    try:
        with open("api_key.txt", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

GEMINI_API_KEY = get_gemini_key()

def authenticate_gsheets(credentials_json="credentials.json"):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_json, scope)
        client = gspread.authorize(creds)
        return client
    except FileNotFoundError:
        return None

def get_sheet(sheet_url):
    client = authenticate_gsheets()
    if not client:
        print("[-] Eroare: credentials.json nu a fost gasit in folder!")
        return None
    return client.open_by_url(sheet_url).sheet1

def analyze_variables(sheet_url):
    sheet = get_sheet(sheet_url)
    if not sheet: return
    try:
        print("[+] Descarc datele...")
        df = pd.DataFrame(sheet.get_all_records())
        print("\n--- RAPORT STATISTIC: TIPURI DE VARIABILE ---")
        for col in df.columns:
            series = df[col].dropna()
            if series.empty: continue
            
            unique_vals = series.nunique()
            if pd.api.types.is_numeric_dtype(series):
                if unique_vals == 2 and set(series.unique()).issubset({0, 1}):
                    print(f"- {col}: Variabila DUMMY (Binara 0/1)")
                elif unique_vals < 10:
                    print(f"- {col}: Variabila DISCRETA / CATEGORIALA")
                else:
                    print(f"- {col}: Variabila CONTINUA")
            else:
                if unique_vals < 15:
                    print(f"- {col}: Variabila CATEGORIALA (Nominala)")
                else:
                    print(f"- {col}: Variabila TEXT (String)")
        print("---------------------------------------------")
    except Exception as e:
        print(f"[-] Eroare la analiza: {e}")

def ask_gemini(question):
    """Conectare Cloud la Gemini 1.5/2.5 Flash Free Tier."""
    if not GEMINI_API_KEY or GEMINI_API_KEY == "PUNE_CHEIA_AICI":
        print("[-] Nu ai introdus cheia API!")
        print("1. Mergi pe https://aistudio.google.com/app/apikey")
        print("2. Creeaza cheia gratuit.")
        print("3. Pune cheia in fisierul 'api_key.txt' din acest folder.")
        return

    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        print("[+] Conectare Gemini (Viteza Fulger)...")
        
        sys_prompt = "Esti un expert in econometrie si statistica universitara. Raspunzi analitic, precis, academic si la obiect (fara introduceri lungi). Formatezi matematic bine."
        
        # Folosim modelul Flash care e extrem de rapid si gratuit
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=question,
            config=genai.types.GenerateContentConfig(
                system_instruction=sys_prompt,
                temperature=0.2 # Raspunsuri analitice stricte
            )
        )
        print(f"\n[🧠 Expert Econometrics]:\n{response.text}")
    except Exception as e:
        print(f"\n[-] Eroare la generare: {e}")
        print("Ai instalat pachetul corect? Ruleaza: pip install google-genai")

def run_local_regression(sheet_url, y_col, x_cols):
    sheet = get_sheet(sheet_url)
    if not sheet: return
    try:
        df = pd.DataFrame(sheet.get_all_records())
        cols_to_use = [y_col] + x_cols
        df = df[cols_to_use].apply(pd.to_numeric, errors='coerce').dropna()
        Y = df[y_col]
        X = sm.add_constant(df[x_cols])
        model = sm.OLS(Y, X).fit()
        print("\n" + "="*50)
        print(" REZULTATE OLS (ZERO-COST LOCAL COMPUTE)")
        print("="*50)
        print(model.summary())
    except Exception as e:
        print(f"[-] Eroare la regresie: {e}")

def interactive_shell(sheet_url):
    print("\n" + "="*70)
    print(" ECONOMETRICS COPILOT - MASTER ARCHITECT (Powered by Gemini API)")
    if sheet_url: print(f" Conectat la baza de date din cloud.")
    print(" Comenzi:")
    print("   /ask [intrebare]     -> Discuta cu Gemini (Viteza maxima)")
    print("   /analyze             -> Scaneaza Sheet-ul (Tipuri de variabile)")
    print("   /regress, /matrix, /test, /clean, /check, /add, ! [cmd]")
    print("="*70)
    
    while True:
        try:
            cmd = input("\nAgent> ").strip()
            if not cmd: continue
            if cmd.lower() in ['/exit', '/quit', 'exit']:
                break
                
            if cmd.startswith("!"):
                sys_cmd = cmd[1:].strip()
                if sys_cmd: subprocess.run(sys_cmd, shell=True)
            elif cmd.startswith("/analyze"):
                if sheet_url: analyze_variables(sheet_url)
                else: print("[-] Ai nevoie de --url.")
            elif cmd.startswith("/ask"):
                question = cmd.replace("/ask", "").strip()
                if question: ask_gemini(question)
                else: print("[-] Scrie o intrebare.")
            
            elif cmd.startswith("/regress"):
                if not sheet_url: continue
                match = re.search(r'/regress\s+(.+?)\s+on\s+(.+)', cmd, re.IGNORECASE)
                if match: run_local_regression(sheet_url, match.group(1).strip(), [x.strip() for x in match.group(2).replace(',', ' ').split()])
            elif cmd.startswith("/matrix"):
                print("=MMULT(MINVERSE(MMULT(TRANSPOSE(X), X)), MMULT(TRANSPOSE(X), Y))")
            elif cmd.startswith("/test"):
                if "bp" in cmd or "hetero" in cmd: print("=BREUSCH_PAGAN_TEST(A2:A100, B2:D100)")
                elif "dw" in cmd or "auto" in cmd: print("=DURBIN_WATSON(E2:E100)")
            elif cmd.startswith("/check"):
                if sheet_url: get_sheet(sheet_url).update(range_name=cmd.replace("/check", "").strip(), values=[[True]])
            elif cmd.startswith("/add"):
                if sheet_url: get_sheet(sheet_url).append_row([x.strip() for x in cmd.replace("/add", "").strip().split(",")])
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"[-] Eroare de sistem: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", type=str, help="URL Google Sheet", required=False, default="")
    args = parser.parse_args()
    interactive_shell(args.url)
