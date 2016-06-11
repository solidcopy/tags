from mutagen.flac import FLAC, Picture

from jp.derevijargon.tags.common.utils import to_int
from jp.derevijargon.tags.file_format.AudioFile import AudioFile
from jp.derevijargon.tags.meta.Image import Image


class FlacFile(AudioFile):
    """
    FLACオーディオファイル
    """

    ALBUM_TAG = "ALBUM"
    """タグ名: アルバムタグ"""
    ALBUM_ARTIST_TAG = "ALBUMARTIST"
    """タグ名: アルバムアーティストタグ"""
    DATE_TAG = "DATE"
    """タグ名: 発売日タグ"""
    DISC_TOTAL_TAG = "DISCTOTAL"
    """タグ名: ディスク数"""

    DISC_NUMBER_TAG = "DISCNUMBER"
    """タグ名: ディスク番号"""
    TRACK_TOTAL_TAG = "TRACKTOTAL"
    """タグ名: トラック数"""

    TRACK_NUMBER_TAG = "TRACKNUMBER"
    """タグ名: トラック番号"""
    TITLE_TAG = "TITLE"
    """タグ名: タイトル"""
    ARTIST_TAG = "ARTIST"
    """タグ名: アーティスト"""


    @classmethod
    def extensions(cls):
        """
        拡張子のタプルを返す。
        """

        return (".flac",)


    def __init__(self, file_path):
        """
        コンストラクタ。
        """
        super().__init__(file_path)


    def init_tags(self, file_path):
        """
        タグ情報をファイルから読み込んでプロパティに設定する。
        """

        # mutagenでFLACのメタ情報を読めるようにする
        flac = FLAC(file_path)

        # アルバム
        self.album = self.get_tag(flac, FlacFile.ALBUM_TAG)
        # アルバムアーティスト
        self.album_artist = self.get_tag(flac, FlacFile.ALBUM_ARTIST_TAG)
        # ディスク数
        self.disc_total = to_int(self.get_tag(flac, FlacFile.DISC_TOTAL_TAG))
        # 発売日
        self.date = self.get_tag(flac, FlacFile.DATE_TAG)

        # ディスク番号
        self.disc_number = to_int(self.get_tag(flac, FlacFile.DISC_NUMBER_TAG))
        # トラック数
        self.track_total = to_int(self.get_tag(flac, FlacFile.TRACK_TOTAL_TAG))

        # トラック番号
        self.track_number = to_int(self.get_tag(flac, FlacFile.TRACK_NUMBER_TAG))
        # タイトル
        self.title = self.get_tag(flac, FlacFile.TITLE_TAG)
        # アーティストリスト
        self.artist_list = self.get_tags(flac, FlacFile.ARTIST_TAG)

        # 画像
        if flac.pictures:
            picture = flac.pictures[0]
            image = Image.create_from_data(picture.mime, picture.data)
            self.image = image


    def get_tag(self, flac, tag):
        """
        指定されたタグの値を文字列として返す。
        複数の値が設定されていた場合は最初の値のみ返す。
        タグが見つからなかった場合はNoneを返す。
        """

        return (self.get_tags(flac, tag) or [None])[0]


    def get_tags(self, flac, tag):
        """
        指定されたタグの値をリストにして返す。
        タグが見つからなかった場合は空のリストを返す。
        """

        return flac.get(tag, [])


    def update_file(self):
        """
        このファイルオブジェクトの内容でオーディオファイルのメタ情報を更新する。
        """

        # mutagenでFLACのメタ情報を開く
        flac = FLAC(self.file_path)

        # 既存のタグと画像を削除する
        flac.clear()
        flac.clear_pictures()

        # アルバム
        flac[FlacFile.ALBUM_TAG] = self.album
        # アルバムアーティスト
        flac[FlacFile.ALBUM_ARTIST_TAG] = self.album_artist
        # 発売日
        flac[FlacFile.DATE_TAG] = self.date
        # ディスク数
        flac[FlacFile.DISC_TOTAL_TAG] = str(self.disc_total)

        # ディスク番号
        flac[FlacFile.DISC_NUMBER_TAG] = str(self.disc_number)
        # トラック数
        flac[FlacFile.TRACK_TOTAL_TAG] = str(self.track_total)

        # トラック番号
        flac[FlacFile.TRACK_NUMBER_TAG] = str(self.track_number)
        # タイトル
        flac[FlacFile.TITLE_TAG] = self.title
        # アーティスト
        flac[FlacFile.ARTIST_TAG] = self.artist_list

        # 画像がある場合
        if self.image:
            # 画像を追加する
            picture = Picture()
            picture.type = 3  # Front Cover
            picture.data = self.image.data
            flac.add_picture(picture)

        # タグの変更を保存する
        flac.save()
