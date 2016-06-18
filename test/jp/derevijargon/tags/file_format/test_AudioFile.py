# coding: utf-8

import unittest
from unittest.mock import MagicMock

from tags.file_format.AudioFile import AudioFile


class Test(unittest.TestCase):
    """
    AudioFileのテストケース。
    """

    def test_init(self):
        """
        コンストラクタをテストする。
        """
        # テスト対象を実行する
        returned_value = AudioFile("/dir/dir/music.flac")

        # 実行結果を検証する
        self.assertEqual(returned_value.file_path, "/dir/dir/music.flac")

    def test_accessors(self):
        """
        アクセサメソッドをテストする。
        """
        # テスト対象
        subject = AudioFile("/dir/dir/music.flac")

        # ファイルパス
        self.assertEqual(subject.get_file_path(), "/dir/dir/music.flac")

    def test_determine_file_name(self):
        """
        determine_file_name()をテストする。
        """
        # テスト対象
        subject = self.create_subject()

        # ディスク番号を付与する
        subject.get_disc_total.return_value = 1
        # ディスク番号のパディングのための呼び出し結果を削除する
        subject.add_zero_paddings = MagicMock(return_value="08")

        # テスト対象を実行する
        returned_value = subject.determine_file_name()

        # 実行結果を検証する
        self.assertEqual(returned_value, "08.sunny-day.flac")

        # トラック番号を付与する
        subject.add_zero_paddings.assert_any_call(8, 15)

        # ファイル名に使用できない文字を代替文字に置換する
        subject.replace_invalid_chars.assert_any_call("08.sunny*day.flac")

    def test_determine_file_name_multi_disc(self):
        """
        determine_file_name()をテストする。
        ディスク数が2以上の場合、ディスク番号がファイル名の先頭に付与されることを確認する。
        """
        # テスト対象
        subject = self.create_subject()

        # ファイル名に使用できない文字を代替文字に置換する
        subject.replace_invalid_chars.return_value = "2.08.sunny-day.flac"

        # テスト対象を実行する
        returned_value = subject.determine_file_name()

        # 実行結果を検証する
        self.assertEqual(returned_value, "2.08.sunny-day.flac")

        # ディスク番号を付与する
        subject.add_zero_paddings.assert_any_call(2, 3)

        # トラック番号を付与する
        subject.add_zero_paddings.assert_any_call(8, 15)

        # ファイル名に使用できない文字を代替文字に置換する
        subject.replace_invalid_chars.assert_any_call("2.08.sunny*day.flac")

    def create_subject(self):
        """
        テスト対象を作成する。
        """
        # テスト対象
        subject = AudioFile("/dir/dir/music.flac")

        # ディスクが複数枚の場合
        subject.get_disc_total = MagicMock(return_value=3)

        # ディスク番号を付与する
        subject.get_disc_number = MagicMock(return_value=2)
        add_zero_paddings_return_value = ["2"]

        # トラック番号を付与する
        subject.get_track_number = MagicMock(return_value=8)
        subject.get_track_total = MagicMock(return_value=15)
        add_zero_paddings_return_value.append("08")

        subject.add_zero_paddings = MagicMock(side_effect=add_zero_paddings_return_value)

        # タイトルを付与する
        subject.get_title = MagicMock(return_value="sunny*day")

        # 拡張子を付与する
        subject.get_extension = MagicMock(return_value=".flac")

        # ファイル名に使用できない文字を代替文字に置換する
        subject.replace_invalid_chars = MagicMock(return_value="08.sunny-day.flac")
        return subject

    def test_add_zero_paddings(self):
        """
        add_zero_paddings(number, max_number)をテストする。
        numberとmax_numberの桁数が異なる場合、0詰めすることを確認する。
        """
        # テスト対象
        subject = AudioFile("xxx")

        # テスト対象を実行する
        returned_value = subject.add_zero_paddings(5, 120)

        # 実行結果を検証する
        self.assertEqual(returned_value, "005")

    def test_add_zero_paddings_no_padding(self):
        """
        add_zero_paddings(number, max_number)をテストする。
        numberとmax_numberの桁数が同じ場合、0詰めしないことを確認する。
        """
        # テスト対象
        subject = AudioFile("xxx")

        # テスト対象を実行する
        returned_value = subject.add_zero_paddings(5, 9)

        # 実行結果を検証する
        self.assertEqual(returned_value, "5")

    def test_replace_invalid_chars(self):
        """
        replace_invalid_chars(file_name)をテストする。
        """
        # テスト対象
        subject = AudioFile("xxx")

        # テスト対象を実行する
        returned_value = subject.replace_invalid_chars("\\fi|le:*\"<na//me>/?")

        # 実行結果を検証する
        self.assertEqual(returned_value, "file-(name)")

if __name__ == "__main__":
    unittest.main()
