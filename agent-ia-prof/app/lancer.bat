@echo off
REM Double-clique sur ce fichier pour lancer Prof IA (Windows).
cd /d "%~dp0"
if not exist .venv (
    echo Premiere installation, patiente quelques minutes...
    python -m venv .venv
    .venv\Scripts\python -m pip install -r requirements.txt
)
REM 0.0.0.0 = accessible aussi depuis le telephone sur le meme Wi-Fi
.venv\Scripts\python -m streamlit run app.py --server.address 0.0.0.0
pause
