# coding: utf-8

import unittest
from unittest.mock import MagicMock, patch, call

from jp.derevijargon.tags.service import rename_service


class Test(unittest.TestCase):
    """
    rename_serviceのテストケース。
    """

    def test_execute(self):
        """
        execute(directory)をテストする。
        """
        # モックを設定する
        find_files = patch("jp.derevijargon.tags.service.rename_service.find_files")
        rename = patch("jp.derevijargon.tags.service.rename_service.os.rename")
        with find_files as find_files, rename as rename:

            # ファイルを検索する
            file1, file2, file3 = MagicMock(), MagicMock(), MagicMock()
            file_list = [file1, file2, file3]
            find_files.return_value = file_list

            # 適切なファイル名を決定する
            file1.determine_file_name.return_value = "1.title.flac"
            file2.determine_file_name.return_value = "2.title.flac"
            file3.determine_file_name.return_value = "3.title.flac"

            # リネームする
            file1.get_file_path.return_value = "xxx"
            file2.get_file_path.return_value = "yyy"
            file3.get_file_path.return_value = "zzz"

            # テスト対象を実行する
            rename_service.execute("/dir/dir")

            # ファイルを検索する
            find_files.assert_any_call("/dir/dir")

            # リネームする
            expected = []
            expected.append(call("xxx", "/dir/dir\\1.title.flac"))
            expected.append(call("yyy", "/dir/dir\\2.title.flac"))
            expected.append(call("zzz", "/dir/dir\\3.title.flac"))
            self.assertSequenceEqual(rename.mock_calls, expected)

if __name__ == "__main__":
    unittest.main()
