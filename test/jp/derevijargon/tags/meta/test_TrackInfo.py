import unittest
from unittest.mock import MagicMock

from tags.meta.TrackInfo import TrackInfo


class Test(unittest.TestCase):
    """
    トラック情報のテストケース。
    """

    def test_init(self):
        """
        コンストラクタをテストする。
        タイトル、アーティストリストの引数がない場合、デフォルト値で初期化されることを確認する。
        """

        # ディスク情報のモック
        disc_info = MagicMock()

        # テスト対象
        subject = TrackInfo(disc_info)

        # ディスク情報
        self.assertIs(subject._disc_info, disc_info)
        # タイトル
        self.assertIsNone(subject._title)
        # アーティスト
        self.assertSequenceEqual(subject._artist_list, [])


    def test_init_with_args(self):
        """
        コンストラクタをテストする。
        """

        # ディスク情報のモック
        disc_info = MagicMock()

        # テスト対象
        subject = TrackInfo(disc_info, "title!", ["art1", "art2"])

        # ディスク情報
        self.assertIs(subject._disc_info, disc_info)
        # タイトル
        self.assertEqual(subject._title, "title!")
        # アーティスト
        self.assertSequenceEqual(subject._artist_list, ["art1", "art2"])


    def test_accessors(self):
        """
        アクセサメソッドをテストする。
        """

        # アルバム情報のモック
        album_info = MagicMock()
        album_info.album_artist = "albumartist!"

        # ディスク情報のモック
        disc_info = MagicMock()
        disc_info.album_info = album_info

        # テスト対象
        subject = TrackInfo(disc_info, "title1", ["art1", "art2"])

        # ディスク情報
        self.assertIs(subject.disc_info, disc_info)
        # トラック番号
        disc_info.track_info_list = ["xxx"] * 2 + [subject] + ["xxx"] * 2
        self.assertEqual(subject.track_number, 3)
        # タイトル
        self.assertEqual(subject.title, "title1")
        # アーティストリスト
        self.assertSequenceEqual(subject.artist_list, ["art1", "art2"])
        subject = TrackInfo(disc_info, "title1")
        self.assertSequenceEqual(subject.artist_list, ["albumartist!"])


if __name__ == "__main__":
    unittest.main()
