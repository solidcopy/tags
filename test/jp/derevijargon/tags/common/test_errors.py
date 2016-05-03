import unittest

from jp.derevijargon.tags.common.errors import UnknownServiceOptionError


class Test(unittest.TestCase):
    """
    errorsモジュールのテストケース。
    """

    def test_UnknownServiceOptionError(self):
        """
        UnknownServiceOptionErrorをテストする。
        """
        e = UnknownServiceOptionError("x")
        self.assertEqual(str(e), "不正なサービス指定です。x")

if __name__ == "__main__":
    unittest.main()
