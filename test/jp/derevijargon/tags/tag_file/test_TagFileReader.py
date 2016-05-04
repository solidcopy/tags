# coding: utf-8

import os
import unittest
from unittest.mock import patch, MagicMock, call

from jp.derevijargon.tags.tag_file.TagFileReader import TagFileReader


class Test(unittest.TestCase):
    """
    TagFileReaderのテストケース。
    """
    # モジュール名
    mod_name = "jp.derevijargon.tags.tag_file.TagFileReader"

    def test_open(self):
        """
        open(directory)をテストする。
        """
        with patch(Test.mod_name + ".TagFileReader") as mock_TagFileReader:

            # テスト対象を実行する
            returned_value = TagFileReader.open("/dir")

            # 実行結果を検証する
            self.assertIs(returned_value, mock_TagFileReader.return_value)

            # ファイルパスがコンストラクタに渡されている
            mock_TagFileReader.assert_any_call("/dir")

    def test_init(self):
        """
        コンストラクタをテストする。
        """
        # テスト対象を実行する
        returned_value = TagFileReader("/dir")

        # 実行結果を検証する
        self.assertEqual(returned_value.directory, "/dir")

    def test_enter(self):
        """
        __enter__()をテストする。
        """
        with patch(Test.mod_name + ".open") as mock_open:

            # テスト対象
            subject = TagFileReader("/dir")

            # openの戻り値を設定する
            mock_open.return_value = "<file>"

            # テスト対象を実行する
            self.assertIs(subject.__enter__(), subject)

            # 実行結果を検証する
            self.assertEqual(subject.file, "<file>")

            # ファイルを開く
            mock_open.assert_any_call(os.path.join("/dir", "tags"), "r", encoding="utf-8", newline="\n")

    def test_exit(self):
        """
        __exit__(exc_type, exc_value, traceback)をテストする。
        """
        # テスト対象
        subject = TagFileReader("/dir")

        # ファイルのモックを設定する
        subject.file = MagicMock()

        # テスト対象を実行する
        subject.__exit__("exc_type", "exc_value", "traceback")

        # ファイルを閉じる
        self.assertTrue(subject.file.close.called)

    def test_reda(self):
        """
        read()をテストする。
        """
        # テスト対象
        subject = TagFileReader("/dir")

        # アルバム情報
        album_info = MagicMock()
        # ディスク情報
        disc_info1 = MagicMock()
        disc_info2 = MagicMock()

        # タグファイルを全行読み込む
        subject.file = MagicMock()
        subject.file.readlines.return_value = ["album!\n", "albumartist!\n", "2016-05-04\n", "\n", "title1-1\n", "title1-2//art1//art2\n", "\n", "title2-1\n"]

        # アルバム情報を作成する
        album_info.create_disc_info = MagicMock(side_effect=[disc_info1, disc_info2])

        # ディスク情報を作成する
        subject.create_album_info = MagicMock(return_value=album_info)

        # テスト対象を実行する
        self.assertIs(subject.read(), album_info)

        # アルバム情報を作成する
        subject.create_album_info.assert_any_call(["album!", "albumartist!", "2016-05-04"])
        # トラック情報を作成する
        self.assertEqual(disc_info1.create_track_info.mock_calls, [call("title1-1", []), call("title1-2", ["art1", "art2"])])
        self.assertEqual(disc_info2.create_track_info.mock_calls, [call("title2-1", [])])

    def test_create_album_info(self):
        """
        create_album_info(lines)をテストする。
        """
        with patch(Test.mod_name + ".AlbumInfo") as AlbumInfo:
            # テスト対象
            subject = TagFileReader("/dir")

            # 画像を読み込む
            subject.load_image = MagicMock(return_value="<image>")

            # テスト対象を実行する
            self.assertIs(subject.create_album_info(["album!", "albumartist!", "2016-05-04"]), AlbumInfo.return_value)

            # 画像を取得する
            self.assertTrue(subject.load_image.called)
            # アルバム情報
            AlbumInfo.assert_any_call("album!", "albumartist!", "2016-05-04", "<image>")

    def test_load_image(self):
        """
        load_image()をテストする。
        """
        with patch(Test.mod_name + ".os.path.exists") as exists, patch(Test.mod_name + ".Image") as Image:
            # テスト対象
            subject = TagFileReader("/dir")

            # 画像の拡張子をループする
            Image.extensions.values.return_value = [".png", ".png", ".jpg"]
            # 画像のファイルパス
            side_effect = [MagicMock(), MagicMock()]
            side_effect[0].get_file_name.return_value = "Folder.png"
            side_effect[1].get_file_name.return_value = "Folder.jpg"
            Image.side_effect = MagicMock(side_effect=side_effect)
            # このファイルが存在する場合
            exists.side_effect = [False, True]
            # 画像を作成してループを抜ける
            Image.create_from_file.return_value = "<image>"

            # テスト対象を実行する
            self.assertEqual(subject.load_image(), "<image>")

            # 実行結果を検証する

            # このファイルが存在する場合
            self.assertEqual(exists.mock_calls, [call("/dir\\Folder.png"), call("/dir\\Folder.jpg")])
            # 画像を作成してループを抜ける
            Image.create_from_file.assert_any_call("/dir\\Folder.jpg")

if __name__ == "__main__":
    unittest.main()
