@echo off
REM This batch file acts as a "shield" to run our Python handler script.
REM It includes detailed logging for debugging purposes.

REM Get the directory where this batch file is located
SET "BATCH_DIR=%~dp0"

REM Define a path for our own debug log file
SET "LOG_FILE=%BATCH_DIR%batch_debug.log"

REM --- Start of Logging ---
echo --- New Run At %TIME% --- > "%LOG_FILE%"
echo Batch file started. >> "%LOG_FILE%"
echo. >> "%LOG_FILE%"

echo Received arguments: %* >> "%LOG_FILE%"
echo. >> "%LOG_FILE%"

echo Calculated BATCH_DIR: %BATCH_DIR% >> "%LOG_FILE%"

SET "PYTHON_HANDLER_SCRIPT=%BATCH_DIR%pwl_core\data_capture\vscode_handler.py"
echo Constructed PYTHON_HANDLER_SCRIPT path: %PYTHON_HANDLER_SCRIPT% >> "%LOG_FILE%"

REM Check if the Python script actually exists at that path
IF EXIST "%PYTHON_HANDLER_SCRIPT%" (
    echo Python handler script FOUND. >> "%LOG_FILE%"
) ELSE (
    echo CRITICAL ERROR: Python handler script NOT FOUND at the specified path. >> "%LOG_FILE%"
    GOTO :EOF
)

SET "VENV_PYTHON=%BATCH_DIR%.venv\Scripts\python.exe"
echo Constructed VENV_PYTHON path: %VENV_PYTHON% >> "%LOG_FILE%"

REM Check if the Python executable actually exists at that path
IF EXIST "%VENV_PYTHON%" (
    echo Virtual env Python executable FOUND. >> "%LOG_FILE%"
) ELSE (
    echo CRITICAL ERROR: Virtual env Python executable NOT FOUND at the specified path. >> "%LOG_FILE%"
    GOTO :EOF
)

echo. >> "%LOG_FILE%"
echo Attempting to execute Python script... >> "%LOG_FILE%"
echo. >> "%LOG_FILE%"

REM Execute the Python script directly, capturing its output
call "%VENV_PYTHON%" "%PYTHON_HANDLER_SCRIPT%" %*

echo. >> "%LOG_FILE%"
echo --- Batch file finished. --- >> "%LOG_FILE%"