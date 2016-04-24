# coding: utf-8

import os

from find_files import find_files

'''
'''
def test_find_files():
    file_list = find_files(r'D:\music\A応P\COSMIC MAGIC STARS')
    for aFile in file_list:
        print(aFile.get_tag('title'))
