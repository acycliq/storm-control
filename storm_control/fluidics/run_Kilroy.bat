@ECHO OFF

SET EXE="C:\Users\experiment\Miniconda3\envs\storm-control\python.exe"
SET KILROY="D:\Dimitris\OneDrive - University College London\dev\Python\storm-control\storm_control\fluidics\kilroy.py"
SET XML="D:\Dimitris\OneDrive - University College London\dev\Python\storm-control\storm_control\fluidics\kilroy_settings_default.xml"

%EXE% %KILROY% %XML%

REM PAUSE
