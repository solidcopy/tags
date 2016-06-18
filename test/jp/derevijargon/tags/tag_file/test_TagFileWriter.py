# coding: utf-8

import os
import unittest
from unittest.mock import patch, MagicMock, call

from tags.tag_file.TagFileWriter import TagFileWriter


class Test(unittest.TestCase):
    """
    TagFileWriterのテストケース。
    """
    # モジュール名
    mod_name = "tags.tag_file.TagFileWriter"

    def test_open(self):
        """
        open(directory)をテストする。
        """
        with patch(Test.mod_name + ".TagFileWriter") as mock_TagFileWriter:

            # テスト対象を実行する
            returned_value = TagFileWriter.open("/dir")

            # 実行結果を検証する
            self.assertIs(returned_value, mock_TagFileWriter.return_value)

            # ファイルパスがコンストラクタに渡されている
            mock_TagFileWriter.assert_any_call("/dir")

    def test_init(self):
        """
        コンストラクタをテストする。
        """
        # テスト対象を実行する
        returned_value = TagFileWriter("/dir")

        # 実行結果を検証する
        self.assertEqual(returned_value.directory, "/dir")

    def test_enter(self):
        """
        __enter__()をテストする。
        """
        with patch(Test.mod_name + ".open") as mock_open:

            # テスト対象
            subject = TagFileWriter("/dir")

            # openの戻り値を設定する
            mock_open.return_value = "<file>"

            # テスト対象を実行する
            self.assertIs(subject.__enter__(), subject)

            # 実行結果を検証する
            self.assertEqual(subject.file, "<file>")

            # ファイルを開く
            mock_open.assert_any_call(os.path.join("/dir", "tags"), "w", encoding="utf-8", newline="\n")

    def test_exit(self):
        """
        __exit__(exc_type, exc_value, traceback)をテストする。
        """
        # テスト対象
        subject = TagFileWriter("/dir")

        # ファイルのモックを設定する
        subject.file = MagicMock()

        # テスト対象を実行する
        subject.__exit__("exc_type", "exc_value", "traceback")

        # ファイルを閉じる
        self.assertTrue(subject.file.close.called)

    def test_write(self):
        """
        write(album_info)をテストする。
        """
        # テスト対象
        subject = TagFileWriter("/dir")

        # ファイル
        subject.file = MagicMock()

        # アルバム情報
        album_info = MagicMock()
        album_info.get_image.return_value = "<image>"
        # ディスク情報
        disc_info1 = MagicMock()
        disc_info2 = MagicMock()
        album_info.get_disc_info_list.return_value = [disc_info1, disc_info2]
        # トラック情報
        disc_info1.get_track_info_list.return_value = ["track1-1", "track1-2"]
        disc_info2.get_track_info_list.return_value = ["track2-1"]

        # アルバム情報を出力する
        subject.write_album_info = MagicMock()
        # トラック情報を出力する
        subject.write_track_info = MagicMock()
        # 画像をファイルに保存する
        subject.write_image = MagicMock()

        # テスト対象を実行する
        subject.write(album_info)

        # アルバム情報を出力する
        subject.write_album_info.assert_any_call(album_info)
        # 空白行を出力する
        self.assertEqual(subject.file.write.mock_calls, [call("\n"), call("\n")])
        # トラック情報を出力する
        self.assertEqual(subject.write_track_info.mock_calls, [call(album_info, "track1-1"), call(album_info, "track1-2"), call(album_info, "track2-1")])
        # 画像をファイルに保存する
        subject.write_image.assert_any_call("<image>")

    def test_write_album_info(self):
        """
        write_album_info(album_info)をテストする。
        """
        # テスト対象
        subject = TagFileWriter("/dir")

        # ファイルをモック化する
        subject.file = MagicMock()

        # アルバム情報
        album_info = MagicMock()
        album_info.get_album.return_value = "album!"
        album_info.get_album_artist.return_value = "albumartist!"
        album_info.get_date.return_value = "2016-05-04"

        # テスト対象を実行する
        subject.write_album_info(album_info)

        # 実行結果を検証する
        self.assertEqual(subject.file.write.mock_calls, [call("album!"), call("\n"), call("albumartist!"), call("\n"), call("2016-05-04"), call("\n")])

    def test_write_track_info(self):
        """
        write_track_info(album_info, track_info)
        アーティストがアルバムアーティストと同じである場合は出力しないことを確認する。
        """
        # テスト対象
        subject = TagFileWriter("/dir")

        # ファイルをモック化する
        subject.file = MagicMock()

        # アルバム情報
        album_info = MagicMock()
        album_info.get_album_artist.return_value = "albumartist!"
        # トラック情報
        track_info = MagicMock()
        track_info.get_title.return_value = "title!"
        track_info.get_artist_list.return_value = ["albumartist!"]

        # テスト対象を実行する
        subject.write_track_info(album_info, track_info)

        # 実行結果を検証する
        self.assertEqual(subject.file.write.mock_calls, [call("title!"), call("\n")])

    def test_write_track_info_with_artists(self):
        """
        write_track_info(album_info, track_info)
        アーティストがアルバムアーティストと異なる場合は出力することを確認する。
        """
        # テスト対象
        subject = TagFileWriter("/dir")

        # ファイルをモック化する
        subject.file = MagicMock()

        # アルバム情報
        album_info = MagicMock()
        album_info.get_album_artist.return_value = "albumartist!"
        # トラック情報
        track_info = MagicMock()
        track_info.get_title.return_value = "title!"
        track_info.get_artist_list.return_value = ["art1", "art2"]

        # テスト対象を実行する
        subject.write_track_info(album_info, track_info)

        # 実行結果を検証する
        self.assertEqual(subject.file.write.mock_calls, [call("title!"), call("//"), call("art1"), call("//"), call("art2"), call("\n")])

    def test_write_image(self):
        """
        write_image(image)をテストする。
        """
        # モックを設定する
        with patch(Test.mod_name + ".open") as mock_open:

            # テスト対象
            subject = TagFileWriter("/dir")

            # 画像
            image = MagicMock()
            image.get_file_name.return_value = "Folder.png"
            image.get_data.return_value = "0xFFFF"

            # ファイルを開く
            image_file = MagicMock()
            mock_open.return_value.__enter__.return_value = image_file

            # テスト対象を実行する
            subject.write_image(image)

            # 画像を出力する
            image_file.write.assert_any_call("0xFFFF")

if __name__ == "__main__":
    unittest.main()
