import unittest
from unittest.mock import MagicMock, patch

from jp.derevijargon.tags.meta.DiscInfo import DiscInfo


class Test(unittest.TestCase):
    """
    ディスク情報のテストケース。
    """
    def test_init(self):
        """
        コンストラクタをテストする。
        """
        # アルバム情報のモック
        album_info = MagicMock()

        # テスト対象
        subject = DiscInfo(album_info)

        # アルバム情報
        self.assertIs(subject.album_info, album_info)
        # トラック情報リスト
        self.assertListEqual(subject.track_info_list, [])

    def test_accessors(self):
        """
        アクセサメソッドをテストする。
        """
        # アルバム情報のモック
        album_info = MagicMock()

        # テスト対象
        subject = DiscInfo(album_info)

        # アルバム情報
        self.assertIs(subject.get_album_info(), album_info)
        # トラック情報リスト
        track_info_list = ["track1", "track2", "track3"]
        subject.track_info_list = track_info_list
        self.assertListEqual(subject.get_track_info_list(), track_info_list)

    def test_get_disc_number(self):
        """
        get_disc_number()をテストする。
        """
        # アルバム情報のモック
        album_info = MagicMock()

        # テスト対象
        subject = DiscInfo(album_info)

        # ディスク情報リストを設定する
        album_info.get_disc_info_list.return_value = [1, 2, 3, subject, 5, 6]

        # テスト対象を実行する
        self.assertEqual(subject.get_disc_number(), 4)

    def test_get_track_total(self):
        """
        get_track_total()をテストする。
        """
        # テスト対象
        subject = DiscInfo()

        # トラック情報を追加する
        subject.track_info_list = [1, 2, 3]

        # テスト対象を実行する
        self.assertEqual(subject.get_track_total(), 3)

    def test_create_track_info(self):
        """
        create_track_info()をテストする。
        """
        # テスト対象
        subject = DiscInfo()

        # トラック情報をモック化する
        with patch("jp.derevijargon.tags.meta.DiscInfo.TrackInfo") as mock:
            # テスト対象を実行する
            returned_value = subject.create_track_info("title!", ["art1", "art2"])

            # トラック情報のコンストラクタが適切な引数で呼ばれた
            mock.assert_any_call(disc_info=subject, title="title!", artist_list=["art1", "art2"])
            # 作成したトラック情報が戻り値である
            self.assertIs(returned_value, mock.return_value)
            # トラック情報がリストに追加されている
            self.assertSequenceEqual(subject.track_info_list, [returned_value])

if __name__ == "__main__":
    unittest.main()
