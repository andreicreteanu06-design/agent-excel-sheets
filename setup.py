from setuptools import setup

setup(
    name='econometrics-copilot',
    version='1.0.0',
    description='Zero-Cost AI Agent for University-Level Econometrics',
    py_modules=['econometrics_agent'],
    install_requires=[
        'gspread',
        'oauth2client',
        'pandas',
        'statsmodels',
        'numpy',
        'google-genai'
    ],
    entry_points={
        'console_scripts': [
            # Aceasta linie transforma scriptul intr-o comanda globala 'econometrics' in terminal
            'econometrics=econometrics_agent:main',
        ],
    },
)
