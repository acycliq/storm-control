@ECHO OFF
SET XML="C:\dev\Python\storm-control\storm_control\fluidics\kilroy_settings_default.xml"

SET ROOT="C:\Users\cortexlab\Anaconda3"
SET EXE="C:\Users\cortexlab\Anaconda3\envs\storm-control\python.exe"
SET KILROY="C:\dev\Python\storm-control\storm_control\fluidics\kilroy.py"
SET PYTHONPATH=%PYTHONPATH%;C:\dev\Python\storm-control

CALL %ROOT%\Scripts\activate.bat storm-control
%EXE% %KILROY% %XML%

PAUSE