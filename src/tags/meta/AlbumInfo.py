from tags.meta.DiscInfo import DiscInfo


class AlbumInfo:
    """
    アルバム情報
    """

    def __init__(self, album=None, album_artist=None, date=None, image=None):
        """
        コンストラクタ。
        """

        # アルバム名
        self._album = album
        # アルバムアーティスト
        self._album_artist = album_artist
        # 発売日
        self._date = date
        # 画像
        self._image = image
        # ディスク情報リスト
        self._disc_info_list = []

    album = property((lambda self: self._album), doc="アルバム")

    album_artist = property((lambda self: self._album_artist), doc="アルバムアーティスト")

    date = property((lambda self: self._date), doc="発売日")

    image = property((lambda self: self._image), doc="画像")

    disc_info_list = property((lambda self: self._disc_info_list[:]), doc="ディスク情報リスト")

    disc_total = property((lambda self: len(self._disc_info_list)), doc="ディスク数")

    def _get_all_track_info_list(self):
        """
        全トラック情報のリストを返す。
        """
        # 全トラック情報リスト
        all_track_info_list = []

        # ディスク情報をループする
        for a_disc_info in self._disc_info_list:
            # トラック情報をリストに追加する
            all_track_info_list.extend(a_disc_info.track_info_list)

        return all_track_info_list

    all_track_info_list = property(_get_all_track_info_list, doc="全トラック情報リスト")


    def create_disc_info(self):
        """
        ディスク情報を作成してリストに追加し、それを返す。
        """

        # ディスク情報を作成する
        disc_info = DiscInfo(album_info=self)

        # ディスク情報をリストに追加する
        self._disc_info_list.append(disc_info)

        return disc_info
