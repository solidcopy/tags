# coding: utf-8

from jp.derevijargon.tags.meta.DiscInfo import DiscInfo


class AlbumInfo:
    """
    アルバム情報
    """
    def __init__(self, album=None, album_artist=None, date=None, image=None):
        """
        コンストラクタ。
        """
        # アルバム名
        self.album = album
        # アルバムアーティスト
        self.album_artist = album_artist
        # 発売日
        self.date = date
        # 画像
        self.image = image
        # ディスク情報リスト
        self.disc_info_list = []

    def get_album(self):
        """アルバム名を返す。"""
        return self.album

    def get_album_artist(self):
        """アルバムアーティストを返す。"""
        return self.album_artist

    def get_date(self):
        """発売日を返す。"""
        return self.date

    def get_image(self):
        """画像を返す。"""
        return self.image

    def get_disc_info_list(self):
        """ディスク情報リストを返す。"""
        return self.disc_info_list[:]

    def create_disc_info(self):
        """
        ディスク情報を作成してリストに追加し、それを返す。
        """
        # ディスク情報を作成する
        disc_info = DiscInfo(album_info=self)

        # ディスク情報をリストに追加する
        self.disc_info_list.append(disc_info)

        return disc_info

    def get_disc_total(self):
        """ディスク数を返す。"""
        return len(self.disc_info_list)

    def get_all_track_info_list(self):
        """
        全トラック情報のリストを返す。
        """
        # 全トラック情報リスト
        all_track_info_list = []

        # ディスク情報をループする
        for a_disc_info in self.disc_info_list:
            # トラック情報をリストに追加する
            all_track_info_list.extend(a_disc_info.get_track_info_list())

        return all_track_info_list
