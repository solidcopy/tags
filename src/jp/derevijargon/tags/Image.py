# coding: utf-8

import os


class Image:
    """
    画像
    """
    # 画像のファイル名
    file_name = "Folder"

    # 画像のMIMEから拡張子への辞書(理由は不明だが、Picture.mimeが空文字列になることが多いのでデフォルトをJPEGにする)
    extensions = {"image/png": ".png", "image/jpeg": ".jpg", "image/jpg": ".jpg", "image/gif": ".gif", "": ".jpg"}

    @classmethod
    def create_from_data(cls, mime, data):
        """
        画像のデータからインスタンスを作成する。
        """
        return Image(Image.extensions[mime], data)

    @classmethod
    def create_from_file(cls, image_file):
        """
        画像ファイルからインスタンスを作成する。
        """
        # 拡張子
        extension = os.path.splitext(image_file)[1]
        # データ
        with open(image_file, "rb") as file:
            data = file.read()

        return Image(extension, data)

    def __init__(self, extension=None, data=None):
        """
        コンストラクタ。
        """
        # 拡張子
        self.extension = extension
        # データ
        self.data = data

    def get_file_name(self):
        """
        ファイル名を返す。
        """
        return Image.file_name + self.extension

    def get_data(self):
        """
        データを返す。
        """
        return self.data
