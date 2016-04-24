# coding: utf-8

import base64

from mutagen.flac import FLAC, Picture

from const import *
from AudioFile import AudioFile
from Image import Image

'''
FLACオーディオファイル
'''
class FlacFile(AudioFile):

    '''
    コンストラクタ。
    '''
    def __init__(self, file):
        AudioFile.__init__(self, file)
        self.flac_file = FLAC(file)

    '''
    指定されたタグの値をリストにして返す。
    タグが見つからなかった場合は空のリストを返す。
    '''
    def get_tags(self, tag):
        return self.flac_file.get(tag, [])

    '''
    指定されたタグの値を文字列として返す。
    複数の値が設定されていた場合は最初の値のみ返す。
    タグが見つからなかった場合はNoneを返す。
    '''
    def get_tag(self, tag):
        return (self.get_tags(tag) or [None])[0]

    '''
    タグを設定する。
    '''
    def set_tag(self, tag, value):
        self.flac_file[tag] = value

    '''
    アートワークの画像を返す。
    '''
    def get_image(self):

        # 画像がなければNoneを返す
        if len(self.flac_file.pictures) == 0:
            return None

        # 画像を作成して返す
        picture = self.flac_file.pictures[0]
        return Image.create_from_data(image_extensions[picture.mime], picture.data)

    '''
    画像を削除する。
    '''
    def remove_images(self):
        self.flac_file.clear_pictures()

    '''
    画像を設定する。
    '''
    def set_image(self, image):
        picture = Picture()
        picture.type = 3 # Front Cover
        picture.data = image.get_data()
        self.flac_file.add_picture(picture)

    '''
    タグを削除する。
    '''
    def remove_tag(self, tag):
        self.flac_file.pop(tag, None)

    '''
    タグの変更を保存する。
    '''
    def save(self):
        self.flac_file.save()
