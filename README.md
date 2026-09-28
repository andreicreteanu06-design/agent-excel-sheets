# Zero-Cost Econometrics Google Sheets Agent

Acest folder conține arhitectura hibridă pentru asistentul tău de econometrie (Google Sheets + Python). Nu implică absolut niciun cost API extern.

## Structura Proiectului

1. **`apps_script.js`**: Conține codul Google Apps Script. 
   - **Cum se folosește**: Copiază tot textul de aici și lipește-l în fișierul tău Google Sheets la secțiunea `Extensions > Apps Script`. Salvează și reîncarcă fișierul Excel. Îți va apărea un meniu nou și vei avea acces la formule custom precum `=DURBIN_WATSON(A2:A100)`.

2. **`econometrics_agent.py`**: Motorul local în Python. Se poate conecta direct la Google Sheets-ul tău în cloud și poate rula regresii (OLS) pe calculatorul tău, fără a plăti pentru OpenAI sau alte servicii cloud (Compute gratuit, local).
   - **Librării folosite**: `gspread` (pentru citirea/scrierea gratuită din Sheets), `statsmodels` (pentru OLS), `pandas`.

## Cum să rulezi partea locală (Python)

**Pasul 1: Instalarea pachetelor**
Deschide un terminal în acest folder și rulează:
```bash
pip install -r requirements.txt
```

**Pasul 2: Conectarea la Google Sheets (Credentials)**
Pentru ca scriptul local să poată citi Google Sheets-ul tău, ai nevoie de un fișier `credentials.json` (Google Cloud Service Account - este 100% gratuit).
1. Mergi pe [Google Cloud Console](https://console.cloud.google.com/).
2. Creează un proiect nou -> Activează API-ul "Google Sheets API" și "Google Drive API".
3. Du-te la Credentials -> Create Credentials -> Service Account.
4. După creare, dă click pe el -> secțiunea "Keys" -> Add Key -> Create new key -> JSON.
5. Salvează fișierul descărcat în acest folder sub numele `credentials.json`.
6. Deschide fișierul `credentials.json`, ia adresa de email (ex: `agent@proiect.iam.gserviceaccount.com`) și dă-i "Share" (Distribuie) direct în Google Sheets-ul tău (cu drept de Editor).

**Pasul 3: Rularea unei regresii local**
Rulează scriptul din consolă:
```bash
python econometrics_agent.py --url "LINK-UL_TAU_GOOGLE_SHEETS" -y NumeleColoaneiY -x ColoanaX1 ColoanaX2
```

Vei primi direct în terminal sumarul econometric complet (R-squared, p-values, t-stat) calculat instant.
