# coding: utf-8

from jp.derevijargon.tags.const import *


class DiscInfo:
    """
    ディスク情報
    """

    def __init__(self):
        """
        コンストラクタ。
        """
        # タグ情報
        self.tags = {}

        """ トラック情報リスト """
        self.track_info_list = []

    def get_track_info_list(self):
        """
        トラック情報リストを返す。
        """
        return self.track_info_list

    def add_track_info(self, track_info):
        """
        トラック情報を追加する。
        """
        self.track_info_list.append(track_info)
        track_number = str(len(self.track_info_list))
        track_info[tag_track_number] = track_number
        self.tags[tag_track_total] = track_number
