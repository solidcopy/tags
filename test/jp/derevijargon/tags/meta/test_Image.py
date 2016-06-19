import unittest
from unittest.mock import patch, MagicMock

from audio_files.Image import Image


class Test(unittest.TestCase):
    """
    Imageのテストケース。
    """

    def test_create_from_data(self):
        """
        create_from_data(mime, data)をテストする。
        """

        with patch("tags.meta.Image.Image") as mock:
            # 戻り値を設定する
            mock.return_value = MagicMock()
            # MIMEと拡張子の対応は実物をそのまま設定する
            mock.EXTENSION_MAP = Image.EXTENSION_MAP

            # テスト対象を実行する
            returned_value = Image.create_from_data("image/png", "xxxdataxxx")

            # Imageのコンストラクタが適切な引数で実行されている
            mock.assert_any_call(".png", "xxxdataxxx")

            # 戻り値を確認する
            self.assertIs(returned_value, mock.return_value)


    def test_create_from_file(self):
        """
        create_from_file(image_file)をテストする。
        """

        # モックを設定する
        with patch("tags.meta.Image.Image") as mock, patch("tags.meta.Image.open") as open_mock:

            # 画像ファイルの読み込みをモック化する
            file = MagicMock()
            file.read.return_value = "xxxdataxxx"
            open_mock.return_value.__enter__.return_value = file

            # テスト対象を実行する
            returned_value = Image.create_from_file("/dir/dir/Folder.png")

            # Imageのコンストラクタが適切な引数で実行されている
            mock.assert_any_call(".png", "xxxdataxxx")
            # 戻り値を確認する
            self.assertIs(returned_value, mock.return_value)


    def test_init(self):
        """
        コンストラクタをテストする。
        """

        # テスト対象を実行する
        returned_value = Image(".png", "xxxdataxxx")

        # 実行結果を検証する
        self.assertEqual(returned_value._extension, ".png")
        self.assertEqual(returned_value._data, "xxxdataxxx")


    def test_accessors(self):
        """
        アクセサメソッドをテストする。
        """

        # テスト対象
        subject = Image(".png", "xxxdataxxx")

        # 拡張子
        self.assertEqual(subject.data, "xxxdataxxx")
        # ファイル名
        self.assertEqual(subject.file_name, "Folder.png")


if __name__ == "__main__":
    unittest.main()
