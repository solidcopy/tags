# coding: utf-8


class AudioFile:
    """
    オーディオファイル
    
    タグへのアクセスなどのAPIを定義するクラス。
    """
    # ファイル名から置換する文字のリスト
    replace_char_list = (("*", "-"), ("\\", ""), ("|", ""), (":", ""), ("\"", ""), ("<", "("), (">", ")"), ("/", ""), ("?", ""))

    def __init__(self, file_path):
        """
        コンストラクタ。
        """
        self.file_path = file_path

    def get_file_path(self):
        """ファイルパスを返す。"""
        return self.file_path

    def determine_file_name(self):
        """
        タグから適切なファイル名を決定する。
        """
        # ファイル名
        file_name = ""

        # ディスクが複数枚の場合
        if 1 < self.get_disc_total():
            # ディスク番号を付与する
            file_name += self.add_zero_paddings(self.get_disc_number(), self.get_disc_total()) + "."

        # トラック番号を付与する
        file_name += self.add_zero_paddings(self.get_track_number(), self.get_track_total()) + "."

        # タイトルを付与する
        file_name += self.get_title()

        # 拡張子を付与する
        file_name += self.get_extension()

        # ファイル名に使用できない文字を代替文字に置換する
        file_name = self.replace_invalid_chars(file_name)

        return file_name

    def add_zero_paddings(self, number, max_number):
        """
        引数numberを引数max_numberと同じ桁数になるように0詰めした文字列を返す。
        """
        # 文字数
        digits_length = len(str(max_number))
        # 書式
        digits_format = "%0" + str(digits_length) + "d"
        # フォーマットする
        digits = digits_format % (number,)

        return digits

    def replace_invalid_chars(self, file_name):
        """
        ファイル名に使用できない文字を代替文字に置換する。
        """
        for src, dest in AudioFile.replace_char_list:
            file_name = file_name.replace(src, dest)

        return file_name
