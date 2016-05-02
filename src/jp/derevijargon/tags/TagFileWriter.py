# coding: utf-8
import os

from jp.derevijargon.tags.const import tag_file_name, artist_separator, tag_file_open_options


class TagFileWriter:
    """
    タグファイル
    """
    @classmethod
    def open(cls, directory):
        """
        タグファイルライターを開く。
        """
        return TagFileWriter(directory)

    def __init__(self, directory):
        """
        コンストラクタ。
        """
        # ディレクトリ
        self.directory = directory

    def __enter__(self):
        # ファイルパス
        file_path = os.path.join(self.directory, tag_file_name)
        # ファイルを開く
        self.file = open(file_path, "w", **tag_file_open_options)
        # 自身を返す
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # ファイルを閉じる
        self.file.close()

    def write(self, album_info):
        """
        タグファイルを出力する。
        """
        # アルバム情報を出力する
        self.write_album_info(album_info)

        # ディスク情報をループする
        for a_disc_info in album_info.get_disc_info_list():
            # 空白行を出力する
            self.file.write("\n")

            # トラック情報をループする
            for a_track_info in a_disc_info.get_track_info_list():
                # トラック情報を出力する
                self.write_track_info(album_info, a_track_info)

        # 画像がある場合
        image = album_info.get_image()
        if image is not None:
            # 画像をファイルに保存する
            self.write_image(image)

    def write_album_info(self, album_info):
        """
        アルバム情報を出力する。
        """
        # アルバム名
        self.file.write(album_info.get_album())
        self.file.write("\n")
        # アルバムアーティスト
        self.file.write(album_info.get_album_artist())
        self.file.write("\n")
        # 発売日
        self.file.write(album_info.get_date())
        self.file.write("\n")

    def write_track_info(self, album_info, track_info):
        """
        トラック情報を出力する。
        """
        # タイトルを出力する
        self.file.write(track_info.get_title())

        # アーティストがアルバムアーティストと異なる場合
        if track_info.get_artist_list() != [album_info.get_album_artist()]:
            # アーティストをループする
            for an_artist in track_info.get_artist_list():
                # 区切りを出力する
                self.file.write(artist_separator)
                # アーティストを出力する
                self.file.write(an_artist)

        # 改行を出力する
        self.file.write("\n")

    def write_image(self, image):
        """
        画像をファイルに保存する。
        """
        with open(os.path.join(self.directory, image.get_file_name()), "wb") as image_file:
            image_file.write(image.get_data())
