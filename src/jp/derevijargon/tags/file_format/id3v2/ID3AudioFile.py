import re

from mutagen.id3 import TALB, TPE2, TPOS, TDRL, TRCK, TIT2, TPE1, APIC

from jp.derevijargon.tags.file_format.AudioFile import AudioFile
from jp.derevijargon.tags.meta.Image import Image


class ID3AudioFile(AudioFile):
    """
    ID3v2タグを使用するオーディオファイルのスーパークラス。
    """

    NUMBER_WITH_TOTAL_PATTERN = re.compile(r"^(\d+)/(\d+)$")
    """番号/総数の正規表現パターン"""

    def __init__(self, file_path):
        """
        コンストラクタ。
        """

        super().__init__(file_path)


    def init_by_id3(self, id3):
        """
        ID3の内容でこのファイルのプロパティを初期化する。
        """

        # アルバム
        self.album = self.get_tag(id3, "TALB")
        # アルバムアーティスト
        self.album_artist = self.get_tag(id3, "TPE2")
        # 発売日
        self.date = self.get_date(id3)
        # ディスク数/ディスク番号
        self.disc_number, self.disc_total = self.parse_number_with_total(self.get_tag(id3, "TPOS"))

        # トラック数/トラック番号
        self.track_number, self.track_total = self.parse_number_with_total(self.get_tag(id3, "TRCK"))

        # タイトル
        self.title = self.get_tag(id3, "TIT2")
        # アーティスト
        self.artist_list = self.get_tags(id3, "TPE1")

        # 画像
        picture = id3.get("APIC:")
        if picture:
            image = Image.create_from_data(picture.mime, picture.data)
            self.image = image


    def get_tag(self, id3, tag):
        """
        フレームのテキスト情報を取得する。
        """

        text_values = self.get_tags(id3, tag)
        return text_values[0] if text_values else None


    def get_tags(self, id3, tag):
        """
        フレームのテキスト情報をすべて取得する。
        """

        frame = id3.get(tag)
        texts = []
        for a_text in frame.text:
            texts.append(a_text)
        return texts


    def get_date(self, id3):
        """
        ID3から発売日を取得する。
        """

        if id3.version == (2, 3, 0):
            year = self.get_tag(id3, "TYER")
            ddmm = self.get_tag(id3, "TDAT")

            # 年と日月が4文字ずつの場合
            if year and len(year) == 4 and ddmm and len(ddmm) == 4:
                return "{}-{}-{}".format(year, ddmm[2:], ddmm[:2])
            return None

        else:
            tdrl = self.get_tag(id3, "TDRL")
            # 時分秒は除外する
            return tdrl.text[:10] if tdrl else None


    def parse_number_with_total(self, value):
        """
        引数を番号と総数に分割する。
        """

        # フィールドがなければどちらもNoneとする
        if not value:
            return (None, None)

        # 総数付きの場合は、番号と総数を返す
        matcher = ID3AudioFile.NUMBER_WITH_TOTAL_PATTERN.match(value)
        if matcher:
            groups = matcher.groups()
            return int(groups[0]), int(groups[1])

        # そうでなければ番号のみ返す
        return int(value), None


    def set_tags_to_id3(self, id3):
        """
        ID3にこのファイルのタグ情報を設定する。
        """

        # 既存のフレームを削除する
        id3.clear()

        # アルバム
        if self.album:
            id3.add(TALB(encoding=3, text=self.album))
        # アルバムアーティスト
        if self.album_artist:
            id3.add(TPE2(encoding=3, text=self.album_artist))
        # 発売日
        if self.date:
            id3.add(TDRL(encoding=3, text=self.date))
        # ディスク番号/ディスク数
        disc_number_total = self.format_number_with_total(self.disc_number, self.disc_total)
        if  disc_number_total:
            id3.add(TPOS(encoding=3, text=disc_number_total))
        # トラック番号/トラック数
        track_number_total = self.format_number_with_total(self.track_number, self.track_total)
        if  track_number_total:
            id3.add(TRCK(encoding=3, text=track_number_total))
        # タイトル
        if self.title:
            id3.add(TIT2(encoding=3, text=self.title))
        # アーティスト
        if self.artist_list:
            id3.add(self.to_tpe1_frame(self.artist_list))
        # 画像
        if self.image:
            id3.add(APIC(mime=self.image.mime, type=3, data=self.image.data, encoding=3, desc=""))


    def format_number_with_total(self, number, total):
        """
        引数を番号と総数に連結する。
        """

        result = (str(number) if number else "") + "/" + (str(total) if total else "")
        return result if result != "/" else None


    def to_tpe1_frame(self, artist_list):
        """
        アーティストリストをTPE1フレームリストに変換する。
        """

        frame = TPE1(encoding=3)
        for an_artist in artist_list:
            frame.append(an_artist)
        return frame
