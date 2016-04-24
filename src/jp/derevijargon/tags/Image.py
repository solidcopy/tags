# coding: utf-8

import os

'''
画像
'''
class Image:

    '''
    コンストラクタ。
    '''
    def __init__(self):
        self.extension = None
        self.data = None

    '''
    コンストラクタ。
    画像のデータから作成する。
    '''
    def create_from_data(extension, data):
        image = Image()
        image.extension = extension
        image.data = data
        return image

    '''
    コンストラクタ。
    画像のファイスパスから作成する。
    '''
    def create_from_file(file_path):
        image = Image()
        # 拡張子
        image.extension = os.path.splitext(file_path)[-1][1:]
        # データを読み込む
        with open(file_path, 'rb') as file:
            image.data = file.read()
        return image

    '''
    拡張子を返す。
    '''
    def get_extension(self):
        return self.extension

    '''
    データを返す。
    '''
    def get_data(self):
        return self.data
