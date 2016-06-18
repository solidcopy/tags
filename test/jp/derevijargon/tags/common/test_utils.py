# coding: utf-8

import unittest

from tags.common.utils import to_int


class Test(unittest.TestCase):
    """
    utilsのテストケース。
    """

    def test_to_int(self):
        """
        to_int(s)をテストする。
        """
        self.assertEqual(to_int("1080"), 1080)

    def test_to_int_None(self):
        """
        to_int(s)をテストする。
        引数がNoneの場合、Noneを返すことを確認する。
        """
        self.assertIsNone(to_int(None))

if __name__ == "__main__":
    unittest.main()
