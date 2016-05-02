# coding: utf-8

from jp.derevijargon.tags.DiscInfo import DiscInfo


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

#     def set_album(self, album):
#         """アルバム名を設定する。"""
#         self.album = album

    def get_album_artist(self):
        """アルバムアーティストを返す。"""
        return self.album_artist

#     def set_album_artist(self, album_artist):
#         """アルバムアーティストを設定する。"""
#         self.album_artist = album_artist

    def get_date(self):
        """発売日を返す。"""
        return self.date

#     def set_date(self, date):
#         """発売日を設定する。"""
#         self.date = date

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

#     def add_disc_info(self, disc_info):
#         """ディスク情報を追加する。"""
#         self.disc_info_list.append(disc_info)
#         disc_info.set_album_info(self)

#     def get_disc_info_by_disc_number(self, disc_number):
#         """
#         指定されたディスク番号のディスク情報があればそれを返す。
#         なければ新しいディスク情報を作成してリストに追加し、そのディスク情報を返す。
#         """
#         # ディスク情報のインデックス
#         disc_info_index = disc_number if disc_number is not None else 0
#
#         # ディスク情報リストを必要なだけ拡張する
#         addition = max(disc_number - len(self.disc_info_list) + 1, 0)
#         self.disc_info_list.extend([None] * addition)
#
#         # 指定されたディスク番号のディスク情報がない場合
#         if self.disc_info_list[disc_info_index] is None:
#             # ディスク情報を作成する
#             self.disc_info_list[disc_info_index](DiscInfo(album_info=self))
#
#         return self.disc_info_list[disc_info_index]

    def get_disc_total(self):
        """ディスク数を返す。"""
        return len(self.disc_info_list)

    def get_number_of_track_infos(self):
        """トラック情報の件数を返す。"""
        return sum([len(x.get_track_info_list()) for x in self.disc_info_list])

#     def set_image(self, image):
#         """
#         画像を設定する。
#         """
#         self.image = image

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
