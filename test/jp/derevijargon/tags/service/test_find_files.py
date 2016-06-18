# coding: utf-8

import os
import unittest
from unittest.mock import patch, MagicMock, call

from tags.service.find_files import find_files


class Test(unittest.TestCase):
    """
    find_filesのテストケース。
    """

    def test_find_files(self):
        """
        find_files(directory)をテストする。
        """
        with patch("tags.service.find_files.glob.glob") as glob \
            , patch("tags.service.find_files.Format") as Format:

            # ファイルのコンストラクタをモック化する
            FlacFile = MagicMock(side_effect=["1.flac", "2.flac", "3.flac"])

            # Format定数の値をモック化する
            Format.__iter__.return_value = [MagicMock(value=dict(ext=".flac", fileClass=FlacFile))]

            # ファイルの検索結果
            file1 = MagicMock()
            file2 = MagicMock()
            file3 = MagicMock()
            glob.return_value = [file1, file2, file3]

            # テスト対象を実行する
            returned_value = find_files("/dir/dir")

            # 実行結果を検証する
            self.assertSequenceEqual(returned_value, ["1.flac", "2.flac", "3.flac"])

            # glob関数が適切な引数で呼ばれている
            glob.assert_any_call(os.path.join("/dir/dir", "*.flac"))

            # ファイルのコンストラクタが適切な引数で呼ばれている
            self.assertSequenceEqual(FlacFile.mock_calls, [call(file1), call(file2), call(file3)])


if __name__ == "__main__":
    unittest.main()
