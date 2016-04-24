# coding: utf-8

from mutagen.flac import FLAC, Picture

from jp.derevijargon.tags.AudioFile import AudioFile
from jp.derevijargon.tags.Image import Image
from jp.derevijargon.tags.const import *


class FlacFile(AudioFile):
    '''
    FLACオーディオファイル
    '''

    def __init__(self, file):
        '''
        コンストラクタ。
        '''
        AudioFile.__init__(self, file)
        self.flac_file = FLAC(file)

    def get_tags(self, tag):
        '''
        指定されたタグの値をリストにして返す。
        タグが見つからなかった場合は空のリストを返す。
        '''
        return self.flac_file.get(tag, [])

    def get_tag(self, tag):
        '''
        指定されたタグの値を文字列として返す。
        複数の値が設定されていた場合は最初の値のみ返す。
        タグが見つからなかった場合はNoneを返す。
        '''
        return (self.get_tags(tag) or [None])[0]

    def set_tag(self, tag, value):
        '''
        タグを設定する。
        '''
        self.flac_file[tag] = value

    def get_image(self):
        '''
        アートワークの画像を返す。
        '''

        # 画像がなければNoneを返す
        if len(self.flac_file.pictures) == 0:
            return None

        # 画像を作成して返す
        picture = self.flac_file.pictures[0]
        return Image.create_from_data(image_extensions[picture.mime], picture.data)

    def remove_images(self):
        '''
        画像を削除する。
        '''
        self.flac_file.clear_pictures()

    def set_image(self, image):
        '''
        画像を設定する。
        '''
        picture = Picture()
        picture.type = 3 # Front Cover
        picture.data = image.get_data()
        self.flac_file.add_picture(picture)

    def remove_tag(self, tag):
        '''
        タグを削除する。
        '''
        self.flac_file.pop(tag, None)

    def save(self):
        '''
        タグの変更を保存する。
        '''
        self.flac_file.save()
