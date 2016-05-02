# coding: utf-8

import os

from jp.derevijargon.tags.meta.AlbumInfo import AlbumInfo
from jp.derevijargon.tags.meta.Image import Image
from jp.derevijargon.tags.tag_file.const import tag_file_name, tag_file_open_options, artist_separator


class TagFileReader:
    """
    タグファイルリーダー
    """
    @classmethod
    def open(cls, directory):
        """
        タグファイルリーダーを開く。
        """
        return TagFileReader(directory)

    def __init__(self, directory):
        """
        コンストラクタ。
        """
        # ディレクトリ
        self.directory = directory

    def __enter__(self):
        """
        withブロック開始時にコールバックされる。
        """
        # ファイルパス
        file_path = os.path.join(self.directory, tag_file_name)
        # ファイルを開く
        self.file = open(file_path, "r", **tag_file_open_options)
        # 自身を返す
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        withブロック終了時にコールバックされる。
        """
        # ファイルを閉じる
        self.file.close()

    def read(self):
        """
        アルバム情報を読み込む。
        """
        # タグファイルを全行読み込む
        lines = [x.rstrip() for x in self.file.readlines()]

        # アルバム情報を作成する
        album_info = self.create_album_info(lines[:3])

        # タグファイルの4行目以降をループする
        for a_line in lines[3:]:

            # 空白行である場合
            if a_line == "":
                # ディスク情報を作成する
                disc_info = album_info.create_disc_info()

            # 空白行ではない場合
            else:
                # タイトルとアーティストリストに分解する
                title, *artist_list = a_line.split(artist_separator)
                # トラック情報を作成する
                disc_info.create_track_info(title, artist_list)

        return album_info
    
    def create_album_info(self, lines):
        """
        タグファイルの最初の3行からアルバム情報を作成する。
        """
        # アルバム、アルバムアーティスト、発売日
        album, album_artist, date = lines
        # 画像を取得する
        image = self.get_image()
        # アルバム情報
        album_info = AlbumInfo(album, album_artist, date, image)

        return album_info

    def get_image(self):
        """
        画像を取得する。
        """
        # 画像の拡張子をループする
        for an_extension in set(Image.extensions.values()):
            # 画像のファイルパス
            image_file_path = os.path.join(self.directory, Image(an_extension).get_file_name())
            # このファイルが存在する場合
            if os.path.exists(image_file_path):
                # 画像を作成してループを抜ける
                return Image.create_from_file(image_file_path)

        return None
