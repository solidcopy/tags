def to_int(s):
    """
    引数sを文字列から数値に変換する。
    sがNoneの場合はNoneを返す。
    """
    return int(s) if s else None

def read_int(file):
    """
    ファイルから4バイト読み込んで数値として返す。
    """
    return read_number(file, 4)

def read_long(file):
    """
    ファイルから4バイト読み込んで数値として返す。
    """
    return read_number(file, 8)

def read_number(file, size):
    """
    ファイルから指定されたバイト数を読み込んで数値として返す。
    """
    return int.from_bytes(file.read(size), "little")
