# coding: utf-8

from enum import Enum

from jp.derevijargon.tags.FlacFile import FlacFile


class Format(Enum):
    """
    オーディオファイルフォーマット
    """
    # FLAC
    flac = {"ext":"flac", "fileClass":FlacFile}
