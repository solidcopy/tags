# coding: utf-8

import jp.derevijargon.tags.common.messages as messages


class UnknownServiceOptionError(BaseException):
    """
    コマンドライン引数のサービス指定が不正である場合に発生するエラー。
    """
    def __init__(self, service_option):
        super().__init__(messages.UNKNOWN_SERVICE_OPTION % (service_option))
