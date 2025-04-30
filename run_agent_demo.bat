@echo off
echo Installing required packages...
pip install -r requirements_demo.txt

echo.
echo Starting Climate Action Orchestrator Agent Demo...
echo.
python agent_realtime_demo.py

echo.
echo Demo completed.
pause
