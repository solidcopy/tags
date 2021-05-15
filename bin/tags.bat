@echo off
set AUDIO_FILES_HOME=%PROJECTS_HOME%\audio_files
set TAGS_HOME=%PROJECTS_HOME%\tags
set PYTHONPATH=%PYTHONPATH%;%TAGS_HOME%\src;%AUDIO_FILES_HOME%\src
call %TAGS_HOME%\.venv\Scripts\activate.bat
@echo on

python -m tags %1

@echo off
call %TAGS_HOME%\.venv\Scripts\deactivate.bat
@echo on
