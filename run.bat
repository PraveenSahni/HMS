@echo off
REM GNU Health Synthetic Data - Windows runner
cd /d "%~dp0"
pip install -q -r requirements.txt
python run_synthetic_data.py %*
