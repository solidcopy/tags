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

#     def get_album_tags(self):
#         """
#         アルバムタグを取得する。
#         """
#         return self.get_tag_info(album_tags)

#     def get_tag_file_album_tags(self):
#         """
#         タグファイル中のアルバムタグを取得する。
#         """
#         return self.get_tag_info(tag_file_album_tags)

#     def get_track_tags(self):
#         """
#         トラックタグを取得する。
#         """
#         return self.get_tag_info(track_tags)

    def get_tag_info(self, target_tags):
        """
        タグを取得する。
        """

        # タグ情報
        tags = {}

        # タグをループする
        for a_tag in target_tags:
            # タグを取得する
            value = self.get_tag(a_tag)
            # タグを辞書に追加する
            tags[a_tag] = value if value is not None else ""

        return tags

    def update(self, tag_info_dict):
        """
        タグ情報を更新する。
        """
        # タグと値をループする
        for a_tag, a_value in tag_info_dict.items():
            # タグを更新する
            self.set_tag(a_tag, a_value)

    def remove_tags(self, tags):
        """
        リストにあるタグを削除する。
        """
        # タグをループする
        for a_tag in tags:
            # 現在の値
            current_value = self.get_tag(a_tag)
            # タグが設定されている場合は削除する
            if current_value is not None:
                self.remove_tag(a_tag)

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
