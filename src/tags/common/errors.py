class UnknownServiceOptionError(Exception):
    """
    コマンドライン引数のサービス指定が不正である場合に発生するエラー。
    """
    def __init__(self, service_option):
        super().__init__("不正なサービス指定です。{}".format(service_option))

