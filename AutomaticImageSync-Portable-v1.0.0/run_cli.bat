@echo off
if not exist "venv" (
    echo Setting up environment...
    python -m venv venv
    call venv\Scripts\activate
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate
)

python cli.py %*
