# coding: utf-8

"""
tagsでは対応していないフォーマットのファイルをオーディオファイルに変換しようとした場合に発生するエラー。
"""
class UnsupportedFormatError(BaseException):

    # 拡張子
    ext = None

    def __init__(self, ext):
        self.ext = ext

    def __str__(self):
        return "サポート対象外のフォーマットです。" + self.ext
