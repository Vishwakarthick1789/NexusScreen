@echo off
echo ===================================================
echo 🚀 Starting NexusScreen AI Environment Setup...
echo ===================================================

if not exist venv (
    echo [1/3] Creating virtual environment...
    python -m venv venv
) else (
    echo [1/3] Virtual environment already exists.
)

echo [2/3] Activating virtual environment...
call venv\Scripts\activate

echo [3/3] Installing requirements...
pip install -r requirements.txt

echo.
echo ===================================================
echo ✅ Setup Complete! Launching NexusScreen...
echo ===================================================
echo [!] NOTE: If you have an OpenAI API key, set it before running for true LLM results.
echo [!] Example: set OPENAI_API_KEY=sk-yourkey
echo.

python app.py
pause
