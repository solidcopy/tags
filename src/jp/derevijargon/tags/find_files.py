# coding: utf-8

import glob
import os

from jp.derevijargon.tags.Format import Format


def find_files(directory):
    '''
    オーディオファイルを検索し、Fileリストとして返す。
    '''

    file_list = []

    for a_format in Format:
        for aFile in glob.glob(os.path.join(directory, '*.' + a_format.value['ext'])):
            fileClass = a_format.value['fileClass']
            newFile = fileClass(aFile)
            file_list.append(newFile)

    return file_list
