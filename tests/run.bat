@echo off

set PYTHON_EXE=

IF NOT EXIST c:\python27\ GOTO python26
set PYTHON_EXE=c:\python27\python.exe
GOTO run

:python26
IF NOT EXIST c:\python26\ GOTO python
set PYTHON_EXE=c:\python26\python.exe
GOTO run

:python
set PYTHON_EXE=python.exe

:run
%PYTHON_EXE% "%~dp0\run_tests.py" %*
pause