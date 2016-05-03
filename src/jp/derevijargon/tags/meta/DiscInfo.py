# coding: utf-8

from jp.derevijargon.tags.meta.TrackInfo import TrackInfo


class DiscInfo:
    """
    ディスク情報
    """
    def __init__(self, album_info=None):
        """
        コンストラクタ。
        """
        # アルバム情報
        self.album_info = album_info
        # トラック情報リスト
        self.track_info_list = []

    def get_album_info(self):
        """アルバム情報を返す。"""
        return self.album_info

    def get_track_info_list(self):
        """トラック情報リストを返す。"""
        return self.track_info_list[:]

    def get_disc_number(self):
        """ディスク番号を返す。"""
        return self.album_info.get_disc_info_list().index(self) + 1

    def get_track_total(self):
        """トラック数を返す。"""
        return len(self.track_info_list)

    def create_track_info(self, title=None, artist_list=None):
        """
        トラック情報を作成してリストに追加し、それを返す。
        """
        # トラック情報を作成する
        track_info = TrackInfo(disc_info=self, title=title, artist_list=artist_list or [])

        # トラック情報をリストに追加する
        self.track_info_list.append(track_info)

        return track_info
