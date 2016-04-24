@echo off
set SRC=%TAGS_HOME%\src
set PYTHONPATH=%SRC%;%PYTHONPATH%
@echo on
python %SRC%\jp\derevijargon\tags\main.py i
python %SRC%\jp\derevijargon\tags\main.py r
