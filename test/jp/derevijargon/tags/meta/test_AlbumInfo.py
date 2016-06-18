import unittest
from unittest.mock import MagicMock, patch

from tags.meta.AlbumInfo import AlbumInfo


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
        self.assertIsNone(subject._album)
        # アルバムアーティスト
        self.assertIsNone(subject._album_artist)
        # 発売日
        self.assertIsNone(subject._date)
        # 画像
        self.assertIsNone(subject._image)
        # ディスク情報リスト
        self.assertListEqual(subject._disc_info_list, [])


    def test_init_with_args(self):
        """
        コンストラクタをテストする。
        引数で属性を初期化する。
        """

        # テスト対象
        subject = AlbumInfo("Album!", "Album Artist!", "2016-05-02", "<image>")

        # アルバム名
        self.assertEqual(subject._album, "Album!")
        # アルバムアーティスト
        self.assertEqual(subject._album_artist, "Album Artist!")
        # 発売日
        self.assertEqual(subject._date, "2016-05-02")
        # 画像
        self.assertEqual(subject._image, "<image>")
        # ディスク情報リスト
        self.assertListEqual(subject._disc_info_list, [])


    def test_accessors(self):
        """
        アクセサメソッドをテストする。
        """

        # テスト対象
        subject = AlbumInfo("Album!", "Album Artist!", "2016-05-02", "<image>")

        # ディスク情報のモックを追加する
        disc_info_list = [MagicMock(), MagicMock(), MagicMock()]
        subject._disc_info_list = disc_info_list[:]

        # トラック情報のダミー値を設定する
        disc_info_list[0].track_info_list = ["a", "b", "c", "d"]
        disc_info_list[1].track_info_list = ["1", "2"]
        disc_info_list[2].track_info_list = ["x", "y", "z"]

        # アルバム名
        self.assertEqual(subject.album, "Album!")
        # アルバムアーティスト
        self.assertEqual(subject.album_artist, "Album Artist!")
        # 発売日
        self.assertEqual(subject.date, "2016-05-02")
        # 画像
        self.assertEqual(subject.image, "<image>")
        # ディスク情報リスト
        self.assertListEqual(subject.disc_info_list, disc_info_list)
        # ディスク数
        self.assertEqual(subject.disc_total, 3)
        # 全トラック情報リスト
        self.assertListEqual(subject.all_track_info_list, ["a", "b", "c", "d", "1", "2", "x", "y", "z"])


    def test_create_disc_info(self):
        """
        create_disc_info()をテストする。
        """

        # テスト対象
        subject = AlbumInfo()

        # 事前にディスク情報を数件追加する
        disc_info1, disc_info2 = MagicMock(), MagicMock()
        subject._disc_info_list = [disc_info1, disc_info2]

        # ディスク情報をモック化する
        with patch("tags.meta.AlbumInfo.DiscInfo") as mock:
            # テスト対象を実行する
            returned_value = subject.create_disc_info()
            # ディスク情報にアルバム情報が設定された
            mock.assert_any_call(album_info=subject)
            # モック化したディスク情報が作成された
            self.assertIs(returned_value, mock.return_value)
            # ディスク情報リストにディスク情報が追加されている
            self.assertListEqual(subject.disc_info_list, [disc_info1, disc_info2, mock.return_value])


if __name__ == "__main__":
    unittest.main()
