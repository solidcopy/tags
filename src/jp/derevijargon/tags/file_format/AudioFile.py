import os


class AudioFile:
    """
    オーディオファイル

    タグへのアクセスなどのAPIを定義するクラス。
    このクラスが定義するメソッドのうち、NotImplementedErrorを送出するものについては、
    サブクラスが適切な実装をおこなう。
    """

    @classmethod
    def extensions(cls):
        """
        拡張子のタプルを返す。
        """

        raise NotImplementedError()


    @classmethod
    def can_handle(cls, file_path):
        """
        指定されたファイルが処理可能かを判定する。
        """

        _, extension = os.path.splitext(file_path)
        return extension.lower() in cls.extensions()


    def __init__(self, file_path):
        """
        コンストラクタ。
        """

        # ファイルパス
        self._file_path = file_path

        self.album = None
        """アルバム"""
        self.album_artist = None
        """アルバムアーティスト"""
        self.disc_total = None
        """ディスク数"""
        self.date = None
        """発売日"""

        self.disc_number = None
        """ディスク番号"""
        self.track_total = None
        """トラック数"""

        self.title = None
        """タイトル"""
        self.track_number = None
        """トラック番号"""
        self.artist_list = None
        """アーティストリスト"""

        self.image = None
        """画像"""

        # タグ情報をファイルから読み込んでプロパティに設定する
        self.init_tags(file_path)

    file_path = property((lambda self: self._file_path), doc="ファイルパス")


    def init_tags(self, file_path):
        """
        タグ情報をファイルから読み込んでプロパティに設定する。
        """

        raise NotImplementedError()


    def update_tags(self, track_info):
        """
        トラック情報からタグを更新する。
        """

        # トラック情報のタグ情報を設定する
        self.init_by_track_info(track_info)

        # タグの変更を保存する
        self.update_file()


    def init_by_track_info(self, track_info):
        """
        トラック情報のタグ情報を設定する。
        """

        # ディスク情報
        disc_info = track_info.disc_info
        # アルバム情報
        album_info = disc_info.album_info

        # アルバム
        self.album = album_info.album
        # アルバムアーティスト
        self.album_artist = album_info.album_artist
        # 発売日
        self.date = album_info.date
        # ディスク枚数
        self.disc_total = album_info.disc_total

        # ディスク番号
        self.disc_number = disc_info.disc_number
        # トラック数
        self.track_total = disc_info.track_total

        # トラック番号
        self.track_number = track_info.track_number
        # タイトル
        self.title = track_info.title
        # アーティストリスト
        self.artist_list = track_info.artist_list

        # 画像
        self.image = album_info.image


    def update_file(self):
        """
        このファイルオブジェクトの内容でオーディオファイルのメタ情報を更新する。
        """

        raise NotImplementedError()


    def has_metadata(self):
        """
        このファイルにタグ情報が何も設定されていなければTrueを返す。
        """

        result = False

        # アルバム
        result = result or self.album
        # アルバムアーティスト
        result = result or self.album_artist
        # 発売日
        result = result or self.date
        # ディスク枚数
        result = result or self.disc_total

        # ディスク番号
        result = result or self.disc_number
        # トラック数
        result = result or self.track_total

        # トラック番号
        result = result or self.track_number
        # タイトル
        result = result or self.title
        # アーティストリスト
        result = result or self.artist_list

        # 画像
        result = result or self.image

        return result
