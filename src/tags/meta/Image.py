import os


class Image:
    """
    画像
    """

    FILE_NAME = "Folder"
    """画像のファイル名"""

    EXTENSION_MAP = {"image/png": ".png", "image/jpeg": ".jpg", "image/jpg": ".jpg", "image/gif": ".gif", "image/bmp": ".bmp", "": ".jpg"}
    """
    画像のMIMEから拡張子への辞書

    理由は不明だが、Picture.mimeが空文字列になることが多いのでデフォルトをJPEGにする。
    """


    @classmethod
    def create_from_data(cls, mime, data):
        """
        画像のデータからインスタンスを作成する。
        """

        return Image(mime, Image.EXTENSION_MAP[mime], data)


    @classmethod
    def create_from_file(cls, image_file_path):
        """
        画像ファイルからインスタンスを作成する。
        """

        # 拡張子
        extension = os.path.splitext(image_file_path)[-1]
        # MIMEタイプ
        mime = Image.determine_mime_by_extension(extension)
        # データ
        with open(image_file_path, "rb") as file:
            data = file.read()

        return Image(mime, extension, data)


    @classmethod
    def determine_mime_by_extension(cls, extension):
        """
        拡張子からMIMEタイプを特定する。
        """

        for a_mime, an_extension in Image.EXTENSION_MAP.items():
            if an_extension == extension:
                return a_mime

        return None


    def __init__(self, mime=None, extension=None, data=None):
        """
        コンストラクタ。
        """

        self._mime = mime
        """MIMEタイプ"""
        self._extension = extension
        """拡張子"""
        self._data = data
        """データ"""

    mime = property((lambda self: self._mime), doc="MIMEタイプ")

    data = property((lambda self: self._data), doc="データ")

    file_name = property((lambda self: Image.FILE_NAME + self._extension), doc="ファイルパス")
