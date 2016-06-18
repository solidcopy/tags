# coding: utf-8

import unittest
from unittest.mock import patch, MagicMock

from tags.service import export_service


class Test(unittest.TestCase):
    """
    export_serviceのテストケース。
    """
    def test_execute(self):
        """
        execute(directory)をテストする。
        """
        # モックを設定する
        with patch("tags.service.export_service.find_files") as find_files \
            , patch("tags.service.export_service.create_album_info") as create_album_info \
            , patch("tags.service.export_service.TagFileWriter") as TagFileWriter:

            # 検索されるファイルリスト
            find_files.return_value = ["file1", "file2"]
            # 作成されるアルバム情報
            album_info = MagicMock()
            create_album_info.return_value = album_info
            # タグファイルライターのモックを設定する
            tag_file = MagicMock()
            TagFileWriter.open.return_value.__enter__.return_value = tag_file

            # テスト対象を実行する
            export_service.execute("/dir/dir")

            # find_files関数が適切な引数で呼ばれた
            find_files.assert_any_call("/dir/dir")
            # create_album_info関数が適切な引数で呼ばれた
            create_album_info.assert_any_call(["file1", "file2"])
            # write関数が適切な引数で呼ばれた
            tag_file.write.asssert_any_call(album_info)

    def test_execute_file_not_found(self):
        """
        execute(directory)をテストする。
        ファイルが1つもない場合、メッセージを出力して終了することを確認する。
        """
        # ファイル検索関数をモック化する
        with patch("tags.service.export_service.find_files") as find_files:

            # ファイルが1件も見つからない
            find_files.return_value = []

            # テスト対象を実行する
            export_service.execute("/dir/dir")

    def test_create_album_info(self):
        """
        create_album_info(file_list)をテストする。
        """

        # ファイルリストを作成する
        file_list = [\
            self.create_file(1, "f1", []), \
            self.create_file(1, "f2", ["art1", "art2"]), \
            self.create_file(2, "f3", []), \
            self.create_file(None, "f4", []), \
            self.create_file(4, "f5", []), \
            self.create_file(2, "f6", []), \
            self.create_file(2, "f7", [])]

        # 1件目
        file = file_list[0]
        file.get_album.return_value = "album!"
        file.get_album_artist.return_value = "albumartist!"
        file.get_date.return_value = "2016-05-03"
        image = MagicMock()
        file.get_image.return_value = image

        # テスト対象を実行する
        returned_value = export_service.create_album_info(file_list)

        # 実行結果を検証する
        self.assertEqual(returned_value.get_album(), "album!")
        self.assertEqual(returned_value.get_album_artist(), "albumartist!")
        # self.assertEqual(returned_value.get_disc_total(), 5)

        # ディスク1
        disc_info = returned_value.get_disc_info_list()[0]
        self.assertEqual(disc_info.get_disc_number(), 1)
        self.assertEqual(disc_info.get_track_total(), 2)

        track_info = disc_info.get_track_info_list()[0]
        self.assertEqual(track_info.get_track_number(), 1)
        self.assertEqual(track_info.get_title(), "f1")
        self.assertEqual(track_info.get_artist_list(), ["albumartist!"])

        track_info = disc_info.get_track_info_list()[1]
        self.assertEqual(track_info.get_track_number(), 2)
        self.assertEqual(track_info.get_title(), "f2")
        self.assertEqual(track_info.get_artist_list(), ["art1", "art2"])

        # ディスク2
        disc_info = returned_value.get_disc_info_list()[1]
        self.assertEqual(disc_info.get_disc_number(), 2)
        self.assertEqual(disc_info.get_track_total(), 1)

        track_info = disc_info.get_track_info_list()[0]
        self.assertEqual(track_info.get_track_number(), 1)
        self.assertEqual(track_info.get_title(), "f3")
        self.assertEqual(track_info.get_artist_list(), ["albumartist!"])

        # ディスク3
        disc_info = returned_value.get_disc_info_list()[2]
        self.assertEqual(disc_info.get_disc_number(), 3)
        self.assertEqual(disc_info.get_track_total(), 1)

        track_info = disc_info.get_track_info_list()[0]
        self.assertEqual(track_info.get_track_number(), 1)
        self.assertEqual(track_info.get_title(), "f4")
        self.assertEqual(track_info.get_artist_list(), ["albumartist!"])

        # ディスク4
        disc_info = returned_value.get_disc_info_list()[3]
        self.assertEqual(disc_info.get_disc_number(), 4)
        self.assertEqual(disc_info.get_track_total(), 1)

        track_info = disc_info.get_track_info_list()[0]
        self.assertEqual(track_info.get_track_number(), 1)
        self.assertEqual(track_info.get_title(), "f5")
        self.assertEqual(track_info.get_artist_list(), ["albumartist!"])

        # ディスク5
        disc_info = returned_value.get_disc_info_list()[4]
        self.assertEqual(disc_info.get_disc_number(), 5)
        self.assertEqual(disc_info.get_track_total(), 2)

        track_info = disc_info.get_track_info_list()[0]
        self.assertEqual(track_info.get_track_number(), 1)
        self.assertEqual(track_info.get_title(), "f6")
        self.assertEqual(track_info.get_artist_list(), ["albumartist!"])

        track_info = disc_info.get_track_info_list()[1]
        self.assertEqual(track_info.get_track_number(), 2)
        self.assertEqual(track_info.get_title(), "f7")
        self.assertEqual(track_info.get_artist_list(), ["albumartist!"])

    def create_file(self, disc_number, title, artist_list):
        """
        ファイルを作成する。
        """
        file = MagicMock()
        file.get_disc_number.return_value = disc_number
        file.get_title.return_value = title
        file.get_artist_list.return_value = artist_list
        return file

if __name__ == "__main__":
    unittest.main()
