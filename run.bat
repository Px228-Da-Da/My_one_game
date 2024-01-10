
@echo off
echo Choose an action:
echo 1: Run the run.py file      --)     .1
echo 2: Py to EXE
set /p choice="Enter action number: "

if "%choice%"=="2" (
    pyinstaller -F --noconsole -n test run.py
) else if "%choice%"=="1" (
    "run.py" python run.py
) else (
    echo Wrong choice
)

