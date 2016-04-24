# coding: utf-8

from jp.derevijargon.tags.const import *


class AudioFile:
    """
    オーディオファイル
    
    タグへのアクセスなどのAPIを定義するクラス。
    """

    def __init__(self, file_path):
        """
        コンストラクタ。
        """
        self.file_path = file_path

    def get_file_path(self):
        """
        ファイルパスを返す。
        """
        return self.file_path

    def get_album_tags(self):
        """
        アルバムタグを取得する。
        """
        return self.get_tag_info(album_tags)

    def get_tag_file_album_tags(self):
        """
        タグファイル中のアルバムタグを取得する。
        """
        return self.get_tag_info(tag_file_album_tags)

    def get_track_tags(self):
        """
        トラックタグを取得する。
        """
        return self.get_tag_info(track_tags)

    def get_tag_info(self, target_tags):
        """
        タグを取得する。
        """

        # タグ情報
        tags = {}

        # タグをループする
        for a_tag in target_tags:
            # タグを取得する
            value = self.get_tag(a_tag)
            # タグを辞書に追加する
            tags[a_tag] = value if value is not None else ""

        return tags

    def update(self, tag_info_dict):
        """
        タグ情報を更新する。
        """
        # タグと値をループする
        for a_tag, a_value in tag_info_dict.items():
            # タグを更新する
            self.set_tag(a_tag, a_value)

    def remove_tags(self, tags):
        """
        リストにあるタグを削除する。
        """
        # タグをループする
        for a_tag in tags:
            # 現在の値
            current_value = self.get_tag(a_tag)
            # タグが設定されている場合は削除する
            if current_value is not None:
                self.remove_tag(a_tag)
