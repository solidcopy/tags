# coding: utf-8

import jp.derevijargon.tags.messages as messages

class UnknownServiceOptionError(BaseException):
    """
    コマンドライン引数のサービス指定が不正である場合に発生するエラー。
    """
    def __init__(self, service_option):
        super().__init__(messages.UNKNOWN_SERVICE_OPTION % (service_option))
        
class UnsupportedFormatError(BaseException):
    """
    tagsでは対応していないフォーマットのファイルをオーディオファイルに変換しようとした場合に発生するエラー。
    """
    # 拡張子
    ext = None

    def __init__(self, ext):
        self.__super__("ex msg")
        self.ext = ext

    def __str__(self):
        return "サポート対象外のフォーマットです。" + self.ext
