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
        """
        ディスク情報を返す。
        """
        return self.disc_info
    
#     def set_disc_info(self, disc_info):
#         """ディスク情報を設定する。"""
#         self.disc_info = disc_info

    def get_title(self):
        """タイトルを返す。"""
        return self.title
    
#     def set_title(self, title):
#         """タイトルを設定する。"""
#         self.title = title
    
    def get_artist_list(self):
        """アーティストリストを返す。"""
        return self.artist_list or [self.disc_info.get_album_info().get_album_artist()]
    
#     def add_artist(self, artist):
#         """アーティストを設定する。"""
#         self.artist_list.append(artist)
    
    def get_track_number(self):
        """トラック番号を返す。"""
        return self.disc_info.get_track_info_list().index(self) + 1
