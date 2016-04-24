# coding: utf-8

import re
import os
import shutil

from const import *

'''
オーディオファイル

タグへのアクセスなどのAPIを定義するクラス。
'''
class AudioFile:

    '''
    コンストラクタ。
    '''
    def __init__(self, file_path):
        self.file_path = file_path

    '''
    ファイルパスを返す。
    '''
    def get_file_path(self):
        return self.file_path

    '''
    アルバムタグを取得する。
    '''
    def get_album_tags(self):
        return self.get_tag_info(album_tags)

    '''
    タグファイル中のアルバムタグを取得する。
    '''
    def get_tag_file_album_tags(self):
        return self.get_tag_info(tag_file_album_tags)

    '''
    トラックタグを取得する。
    '''
    def get_track_tags(self):
        return self.get_tag_info(track_tags)

    '''
    タグを取得する。
    '''
    def get_tag_info(self, target_tags):

        # タグ情報
        tags = {}

        # タグをループする
        for a_tag in target_tags:
            # タグを取得する
            value = self.get_tag(a_tag)
            # タグを辞書に追加する
            tags[a_tag] = value if value is not None else ''

        return tags

    '''
    タグ情報を更新する。
    '''
    def update(self, tag_info_dict):
        # タグと値をループする
        for a_tag, a_value in tag_info_dict.items():
            # タグを更新する
            self.set_tag(a_tag, a_value)

    '''
    リストにあるタグを削除する。
    '''
    def remove_tags(self, tags):
        # タグをループする
        for a_tag in tags:
            # 現在の値
            current_value = self.get_tag(a_tag)
            # タグが設定されている場合は削除する
            if current_value is not None:
                self.remove_tag(a_tag)
