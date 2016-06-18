# coding: utf-8

import unittest
from unittest.mock import patch, MagicMock

from tags.service import import_service


class Test(unittest.TestCase):
    """
    import_serviceのテストケース。
    """

    def test_execute(self):
        """
        execute(directory)をテストする。
        """
        # モックを設定する
        find_files = patch("tags.service.import_service.find_files")
        TagFileReader = patch("tags.service.import_service.TagFileReader")
        with find_files as find_files, TagFileReader as TagFileReader:

            # ファイルを検索する
            file1, file2, file3 = MagicMock(), MagicMock(), MagicMock()
            find_files.return_value = [file1, file2, file3]

            # タグファイルからアルバム情報を読み込む
            album_info = MagicMock()

            tag_file = MagicMock()
            tag_file.read.return_value = album_info

            TagFileReader.open.return_value.__enter__.return_value = tag_file

            # このアルバム情報の全トラック情報リスト
            album_info.get_all_track_info_list.return_value = ["t1", "t2", "t3"]

            # テスト対象を実行する
            import_service.execute("/dir/dir")

            # ファイルを検索する
            find_files.assert_any_call("/dir/dir")

            # タグファイルからアルバム情報を読み込む
            TagFileReader.open.assert_any_call("/dir/dir")

            # タグを更新する
            file1.update_tags.assert_any_call("t1")
            file2.update_tags.assert_any_call("t2")
            file3.update_tags.assert_any_call("t3")

if __name__ == "__main__":
    unittest.main()
