# coding: utf-8

import glob
import os

from Format import Format

'''
オーディオファイルを検索し、Fileリストとして返す。
'''
def find_files(directory):

    file_list = []

    for a_format in Format:
        for aFile in glob.glob(os.path.join(directory, '*.' + a_format.value['ext'])):
            fileClass = a_format.value['fileClass']
            newFile = fileClass(aFile)
            file_list.append(newFile)

    return file_list
