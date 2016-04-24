# coding: utf-8

from enum import Enum

from FlacFile import FlacFile

class Format(Enum):
    flac = {'ext':'flac', 'fileClass':FlacFile}
