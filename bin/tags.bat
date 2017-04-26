@echo off
set AUDIO_FILES_HOME=%PROJECTS_HOME%\audio_files
set PYTHONPATH=%TAGS_HOME%\src;%AUDIO_FILES_HOME%\src
@echo on

@echo off
call %TAGS_HOME%\bin\env\Scripts\activate.bat
@echo on

python %TAGS_HOME%\src\tags\main.py %1

@echo off
call %TAGS_HOME%\bin\env\Scripts\deactivate.bat
@echo on
