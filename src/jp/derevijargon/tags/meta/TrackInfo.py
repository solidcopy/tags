# coding: utf-8

class TrackInfo:
    """
    トラック情報
    """
    def __init__(self, disc_info=None, title=None, artist_list=None):
        """
        コンストラクタ。
        """
        # ディスク情報
        self.disc_info = disc_info
        # タイトル
        self.title = title
        # アーティストリスト
        self.artist_list = artist_list or []

    def get_disc_info(self):
        """ディスク情報を返す。"""
        return self.disc_info

    def get_title(self):
        """タイトルを返す。"""
        return self.title

    def get_artist_list(self):
        """アーティストリストを返す。"""
        return self.artist_list or [self.disc_info.get_album_info().get_album_artist()]

    def get_track_number(self):
        """トラック番号を返す。"""
        return self.disc_info.get_track_info_list().index(self) + 1
