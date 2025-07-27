@echo off
cd /d "%~dp0"
set PYTHONPATH=%cd%\site-packages
Python310\python.exe BalloonPop.py
pause
