# coding: utf-8

from mutagen.flac import FLAC, Picture

from jp.derevijargon.tags.AudioFile import AudioFile
from jp.derevijargon.tags.Image import Image
from jp.derevijargon.tags.utils import to_int


class FlacFile(AudioFile):
    """
    FLACオーディオファイル
    """
    # タグ名
    album_tag = "ALBUM"
    album_artist_tag = "ALBUMARTIST"
    date_tag = "DATE"
    disc_total_tag = "DISCTOTAL"

    disc_number_tag = "DISCNUMBER"
    track_total_tag = "TRACKTOTAL"

    track_number_tag = "TRACKNUMBER"
    title_tag = "TITLE"
    artist_tag = "ARTIST"

    def __init__(self, file):
        """
        コンストラクタ。
        """
        super().__init__(file)
        self.flac_file = FLAC(file)

    def get_album(self):
        """アルバム名を返す。"""
        return self.get_tag(FlacFile.album_tag)

    def set_album(self, album):
        """アルバム名を設定する。"""
        self.set_tag(FlacFile.album_tag, album)

    def get_album_artist(self):
        """アルバムアーティストを返す。"""
        return self.get_tag(FlacFile.album_artist_tag)

    def set_album_artist(self, album_artist):
        """アルバムアーティストを設定する。"""
        self.set_tag(FlacFile.album_artist_tag, album_artist)

    def get_date(self):
        """発売日を返す。"""
        return self.get_tag(FlacFile.date_tag)

    def set_date(self, date):
        """発売日を設定する。"""
        self.set_tag(FlacFile.date_tag, date)

    def get_disc_total(self):
        """ディスク数を返す。"""
        return to_int(self.get_tag(FlacFile.disc_total_tag))

    def set_disc_total(self, disc_total):
        """ディスク数を設定する。"""
        self.set_tag(FlacFile.disc_total_tag, str(disc_total))

    def get_disc_number(self):
        """ディスク番号を返す。"""
        return to_int(self.get_tag(FlacFile.disc_number_tag))

    def set_disc_number(self, disc_number):
        """ディスク番号を設定する。"""
        self.set_tag(FlacFile.disc_number_tag, str(disc_number))

    def get_track_total(self):
        """トラック数を返す。"""
        return to_int(self.get_tag(FlacFile.track_total_tag))

    def set_track_total(self, track_total):
        """トラック数を設定する。"""
        self.set_tag(FlacFile.track_total_tag, str(track_total))

    def get_track_number(self):
        """トラック番号を返す。"""
        return to_int(self.get_tag(FlacFile.track_number_tag))

    def set_track_number(self, track_number):
        """トラック番号を設定する。"""
        self.set_tag(FlacFile.track_number_tag, str(track_number))

    def get_title(self):
        """タイトルを返す。"""
        return self.get_tag(FlacFile.title_tag)

    def set_title(self, title):
        """タイトルを設定する。"""
        self.set_tag(FlacFile.title_tag, title)

    def get_artist_list(self):
        """アーティストリストを返す。"""
        return self.get_tags(FlacFile.artist_tag)

    def set_artist_list(self, artist_list):
        """アーティストリストを設定する。"""
        self.set_tag(FlacFile.artist_tag, artist_list)

    def get_tags(self, tag):
        """
        指定されたタグの値をリストにして返す。
        タグが見つからなかった場合は空のリストを返す。
        """
        return self.flac_file.get(tag, [])

    def get_tag(self, tag):
        """
        指定されたタグの値を文字列として返す。
        複数の値が設定されていた場合は最初の値のみ返す。
        タグが見つからなかった場合はNoneを返す。
        """
        return (self.get_tags(tag) or [None])[0]

    def set_tag(self, tag, value):
        """
        タグを設定する。
        """
        self.flac_file[tag] = value

    def get_image(self):
        """
        アートワークの画像を返す。
        """
        # 画像がなければNoneを返す
        if len(self.flac_file.pictures) == 0:
            return None

        # 画像を作成して返す
        picture = self.flac_file.pictures[0]
        return Image.create_from_data(picture.mime, picture.data)

    def set_image(self, image):
        """
        画像を設定する。
        """
        picture = Picture()
        picture.type = 3  # Front Cover
        picture.data = image.get_data()
        self.flac_file.add_picture(picture)

    def update_tags(self, track_info):
        """
        トラック情報からタグを更新する。
        """
        # 既存のタグと画像を削除する
        self.flac_file.clear()
        self.flac_file.clear_pictures()

        # トラック情報のタグ情報を設定する
        self.set_tags_by_track_info(track_info)

        # タグの変更を保存する
        self.flac_file.save()

    def set_tags_by_track_info(self, track_info):
        """
        トラック情報のタグ情報を設定する。
        """
        # ディスク情報
        disc_info = track_info.get_disc_info()
        # アルバム情報
        album_info = disc_info.get_album_info()

        # アルバム
        self.set_album(album_info.get_album())
        # アルバムアーティスト
        self.set_album_artist(album_info.get_album_artist())
        # 発売日
        self.set_date(album_info.get_date())
        # 画像
        self.set_image(album_info.get_image())
        # ディスク枚数
        self.set_disc_total(album_info.get_disc_total())

        # ディスク番号
        self.set_disc_number(disc_info.get_disc_number())
        # トラック数
        self.set_track_total(disc_info.get_track_total())

        # トラック番号
        self.set_track_number(track_info.get_track_number())
        # タイトル
        self.set_title(track_info.get_title())
        # アーティストリスト
        self.set_artist_list(track_info.get_artist_list())

    def get_extension(self):
        """
        拡張子を返す。
        """
        return ".flac"
