# coding: utf-8

import unittest
from unittest.mock import MagicMock

from jp.derevijargon.tags.meta.TrackInfo import TrackInfo


class Test(unittest.TestCase):
    """
    トラック情報のテストケース。
    """
    def test_init(self):
        """
        コンストラクタをテストする。
        引数がない場合、デフォルト値で初期化されることを確認する。
        """
        # テスト対象
        subject = TrackInfo()

        # ディスク情報
        self.assertIsNone(subject.disc_info)
        # タイトル
        self.assertIsNone(subject.title)
        # アーティスト
        self.assertSequenceEqual(subject.artist_list, [])

    def test_init_with_args(self):
        """
        コンストラクタをテストする。
        """
        # ディスク情報のモック
        disc_info = MagicMock()

        # テスト対象
        subject = TrackInfo(disc_info, "title!", ["art1", "art2"])

        # ディスク情報
        self.assertIs(subject.disc_info, disc_info)
        # タイトル
        self.assertEqual(subject.title, "title!")
        # アーティスト
        self.assertSequenceEqual(subject.artist_list, ["art1", "art2"])

    def test_accessors(self):
        """
        アクセサメソッドをテストする。
        """
        # ディスク情報のモック
        disc_info = MagicMock()

        # テスト対象
        subject = TrackInfo(disc_info, "title1")

        # ディスク情報
        self.assertIs(subject.disc_info, disc_info)
        # タイトル
        self.assertEqual(subject.get_title(), "title1")

    def test_get_artist_list(self):
        """
        get_artist_list()をテストする。
        アーティストリストが空でなければ、そのまま返すことを確認する。
        """
        # テスト対象
        subject = TrackInfo(artist_list=["art1", "art2"])

        # テスト対象を実行する
        self.assertSequenceEqual(subject.get_artist_list(), ["art1", "art2"])

    def test_get_artist_list_unset(self):
        """
        get_artist_list()をテストする。
        アーティストリストが空なら、アルバムアーティストを唯一の要素とするリストを返すことを確認する。
        """
        # アルバム情報をモック化する
        album_info = MagicMock()
        album_info.get_album_artist.return_value = "albumartist!"

        # ディスク情報をモック化する
        disc_info = MagicMock()
        disc_info.get_album_info.return_value = album_info

        # テスト対象
        subject = TrackInfo(disc_info)

        # テスト対象を実行する
        self.assertSequenceEqual(subject.get_artist_list(), ["albumartist!"])

    def test_get_track_number(self):
        """
        get_track_number()をテストする。
        """
        # ディスク情報をモック化する
        disc_info = MagicMock()

        # テスト対象
        subject = TrackInfo(disc_info)

        # トラック情報リストを設定する
        disc_info.get_track_info_list.return_value = ["xxx"] * 11 + [subject] + ["xxx"] * 3

        # テスト対象を実行する
        self.assertEqual(subject.get_track_number(), 12)

if __name__ == "__main__":
    unittest.main()
