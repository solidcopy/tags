# coding: utf-8

import os


class Image:
    """
    画像
    """

    def __init__(self):
        """
        コンストラクタ。
        """
        self.extension = None
        self.data = None

    def create_from_data(extension, data):
        """
        コンストラクタ。
        画像のデータから作成する。
        """
        image = Image()
        image.extension = extension
        image.data = data
        return image

    def create_from_file(file_path):
        """
        コンストラクタ。
        画像のファイスパスから作成する。
        """
        image = Image()
        # 拡張子
        image.extension = os.path.splitext(file_path)[-1][1:]
        # データを読み込む
        with open(file_path, "rb") as file:
            image.data = file.read()
        return image

    def get_extension(self):
        """
        拡張子を返す。
        """
        return self.extension

    def get_data(self):
        """
        データを返す。
        """
        return self.data
