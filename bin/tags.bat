@echo off
set SRC=%TAGS_HOME%\src
set PYTHONPATH=%SRC%;%PYTHONPATH%
@echo on
python %SRC%\jp\derevijargon\tags\main.py %1
