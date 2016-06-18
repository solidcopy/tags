@echo off
set AUDIO_FILES_HOME=%PROJECTS_HOME%\audio_files
set PYTHONPATH=%TAGS_HOME%\src;%AUDIO_FILES_HOME%\src
@echo on
python %TAGS_HOME%\src\tags\main.py %1
