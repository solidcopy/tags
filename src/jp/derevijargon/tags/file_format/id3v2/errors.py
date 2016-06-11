class ID3v2FormatError(Exception):
    """
    ID3v2の形式に違反している場合に発生するエラー。
    """

    def __init__(self, description):
        """
        コンストラクタ。
        """

        super().__init__(description)

        # 詳細
        self._description = description

    description = property((lambda self: self._description), doc="詳細")
