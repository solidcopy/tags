from tags.meta.TrackInfo import TrackInfo


class DiscInfo:
    """
    ディスク情報
    """

    def __init__(self, album_info):
        """
        コンストラクタ。
        """
        # アルバム情報
        self._album_info = album_info
        # トラック情報リスト
        self._track_info_list = []

    disc_number = property((lambda self: self._album_info.disc_info_list.index(self) + 1), doc="ディスク番号")

    album_info = property((lambda self: self._album_info), doc="アルバム情報")

    track_info_list = property((lambda self: self._track_info_list[:]), doc="トラック情報リスト")

    track_total = property((lambda self: len(self._track_info_list)), doc="トラック数")


    def create_track_info(self, title=None, artist_list=None):
        """
        トラック情報を作成してリストに追加し、それを返す。
        """
        # トラック情報を作成する
        track_info = TrackInfo(disc_info=self, title=title, artist_list=artist_list)

        # トラック情報をリストに追加する
        self._track_info_list.append(track_info)

        return track_info
