class TrackInfo:
    """
    トラック情報
    """

    def __init__(self, disc_info, title=None, artist_list=None):
        """
        コンストラクタ。
        """

        # ディスク情報
        self._disc_info = disc_info
        # タイトル
        self._title = title
        # アーティストリスト
        self._artist_list = artist_list or []

    disc_info = property((lambda self: self._disc_info), doc="ディスク情報")

    track_number = property((lambda self: self._disc_info.track_info_list.index(self) + 1), doc="トラック番号")

    title = property((lambda self: self._title), doc="タイトル")

    artist_list = property((lambda self: self._artist_list[:] or [self._disc_info.album_info.album_artist]), doc="アーティストリスト")
