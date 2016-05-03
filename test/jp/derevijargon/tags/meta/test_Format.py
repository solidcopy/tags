# coding: utf-8

import unittest

from jp.derevijargon.tags.meta.Format import Format
from jp.derevijargon.tags.tag_file.FlacFile import FlacFile


class Test(unittest.TestCase):
    """
    Formatのテストケース。
    """

    def test_flac(self):
        """
        flacの内容をテストする。
        """
        self.assertEqual(Format.flac.value["ext"], ".flac")
        self.assertEqual(Format.flac.value["fileClass"], FlacFile)

if __name__ == "__main__":
    unittest.main()