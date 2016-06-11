class AudioFileFormatError(Exception):
    """
    オーディオファイル形式エラー

    オーディオファイルの形式が仕様に違反している場合に発生するエラー。
    """

    def __init__(self, file_path=None, file_format=None, description=None):
        """
        コンストラクタ。
        """

        super().__init__("ファイル形式が不正です。ファイルパス\"{}\" 形式\"{}\", 詳細\"{}\"".format(file_path, file_format, description))


class UnsupportedAudioFileFormatError(Exception):
    """
    オーディオファイル形式未対応エラー

    オーディオファイルの形式が未知のものである場合に発生するエラー。
    """

    def __init__(self, file_path):
        """
        コンストラクタ。
        """

        super().__init__("未対応のファイル形式です。ファイルパス\"{}\"".format(file_path))
