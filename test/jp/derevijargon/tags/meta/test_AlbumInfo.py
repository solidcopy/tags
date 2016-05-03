import unittest
from unittest.mock import MagicMock, patch

from jp.derevijargon.tags.meta.AlbumInfo import AlbumInfo
from jp.derevijargon.tags.meta.DiscInfo import DiscInfo


class Test(unittest.TestCase):
    """
    アルバム情報のテストケース
    """
    def test_init(self):
        """
        コンストラクタをテストする。
        """
        # テスト対象
        subject = AlbumInfo()

        # アルバム名
        self.assertIsNone(subject.album)
        # アルバムアーティスト
        self.assertIsNone(subject.album_artist)
        # 発売日
        self.assertIsNone(subject.date)
        # 画像
        self.assertIsNone(subject.image)
        # ディスク情報リスト
        self.assertListEqual(subject.disc_info_list, [])

    def test_init_with_args(self):
        """
        コンストラクタをテストする。
        引数で属性を初期化する。
        """
        # テスト対象
        subject = AlbumInfo("Album!", "Album Artist!", "2016-05-02", "<image>")

        # アルバム名
        self.assertEqual(subject.album, "Album!")
        # アルバムアーティスト
        self.assertEqual(subject.album_artist, "Album Artist!")
        # 発売日
        self.assertEqual(subject.date, "2016-05-02")
        # 画像
        self.assertEqual(subject.image, "<image>")
        # ディスク情報リスト
        self.assertListEqual(subject.disc_info_list, [])

    def test_accessors(self):
        """
        アクセサメソッドをテストする。
        """
        # テスト対象
        subject = AlbumInfo("Album!", "Album Artist!", "2016-05-02", "<image>")
        disc_info_list = []
        with patch("jp.derevijargon.tags.meta.DiscInfo"):
            disc_info_list.append(subject.create_disc_info())

        # アルバム名
        self.assertEqual(subject.get_album(), "Album!")
        # アルバムアーティスト
        self.assertEqual(subject.get_album_artist(), "Album Artist!")
        # 発売日
        self.assertEqual(subject.get_date(), "2016-05-02")
        # 画像
        self.assertEqual(subject.get_image(), "<image>")
        # ディスク情報リスト
        self.assertListEqual(subject.get_disc_info_list(), disc_info_list)

    def test_create_disc_info(self):
        """
        create_disc_info()をテストする。
        """
        # テスト対象
        subject = AlbumInfo()

        # 事前にディスク情報を数件追加する
        disc_info1, disc_info2 = DiscInfo(), DiscInfo()
        subject.disc_info_list = [disc_info1, disc_info2]

        # ディスク情報をモック化する
        with patch("jp.derevijargon.tags.meta.AlbumInfo.DiscInfo") as mock:
            # テスト対象を実行する
            returned_value = subject.create_disc_info()
            # ディスク情報にアルバム情報が設定された
            mock.assert_any_call(album_info=subject)
            # モック化したディスク情報が作成された
            self.assertIs(returned_value, mock.return_value)
            # ディスク情報リストにディスク情報が追加されている
            self.assertListEqual(subject.disc_info_list, [disc_info1, disc_info2, mock.return_value])

    def test_get_disc_total(self):
        """
        get_disc_total()をテストする。
        """
        # テスト対象
        subject = AlbumInfo()

        # 適当にディスク情報を追加する
        subject.disc_info_list = [DiscInfo(), DiscInfo(), DiscInfo(), DiscInfo(), DiscInfo()]

        # テスト対象を実行する
        self.assertEqual(subject.get_disc_total(), 5)

    def test_get_all_track_info_list(self):
        """
        get_all_track_info_list()をテストする。
        """
        # テスト対象
        subject = AlbumInfo()

        # ディスク情報のモックを追加する
        subject.disc_info_list = [MagicMock(), MagicMock(), MagicMock()]

        # トラック情報のダミー値を設定する
        subject.disc_info_list[0].get_track_info_list.return_value = ["a", "b", "c", "d"]
        subject.disc_info_list[1].get_track_info_list.return_value = ["1", "2"]
        subject.disc_info_list[2].get_track_info_list.return_value = ["x", "y", "z"]

        # テスト対象を実行する
        self.assertEqual(subject.get_all_track_info_list(), ["a", "b", "c", "d", "1", "2", "x", "y", "z"])

    def test_get_all_track_info_list_empty(self):
        """
        get_all_track_info_list()をテストする。
        ディスク情報が0件の場合、空のリストを返すことを確認する。
        """
        # テスト対象
        subject = AlbumInfo()

        # テスト対象を実行する
        self.assertEqual(subject.get_all_track_info_list(), [])

if __name__ == "__main__":
    unittest.main()
