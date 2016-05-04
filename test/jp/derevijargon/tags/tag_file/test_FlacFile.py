# coding: utf-8

import unittest
from unittest.mock import patch, MagicMock

from jp.derevijargon.tags.tag_file.FlacFile import FlacFile


class Test(unittest.TestCase):
    """
    FlacFileのテストケース。
    """
    def setUp(self):
        """
        テストを準備する。
        """
        # モックを設定する
        self.init = patch("jp.derevijargon.tags.tag_file.FlacFile.AudioFile.__init__")
        self.FLAC = patch("jp.derevijargon.tags.tag_file.FlacFile.FLAC")
        self.Picture = patch("jp.derevijargon.tags.tag_file.FlacFile.Picture")
        self.Image = patch("jp.derevijargon.tags.tag_file.FlacFile.Image")

    def test_init(self):
        """
        コンストラクタをテストする。
        """
        # モックを設定する
        with self.init as init, self.FLAC as FLAC:

            # FLACの戻り値を設定する
            FLAC.return_value = "flacfile"

            # テスト対象を実行する
            subject = FlacFile("xxx.flac")

            # 実行結果を検証する

            # AudioFileのコンストラクタにファイルパスが渡されている
            init.assert_any_call("xxx.flac")
            # FLACの戻り値が設定されている
            self.assertEqual(subject.flac_file, "flacfile")

    def test_get_album(self):
        """
        get_album()をテストする。
        """
        # モックを設定する
        with self.init, self.FLAC:

            # テスト対象
            subject = FlacFile("xxx.flac")

            # 戻り値を設定する
            subject.get_tag = MagicMock(return_value="album!")

            # テスト対象を実行する
            self.assertEqual(subject.get_album(), "album!")

            # タグ名を検証する
            subject.get_tag.assert_any_call("ALBUM")

    def test_set_album(self):
        """
        set_album(album)をテストする。
        """
        # モックを設定する
        with self.init, self.FLAC:

            # テスト対象
            subject = FlacFile("xxx.flac")

            # 戻り値を設定する
            subject.set_tag = MagicMock()

            # テスト対象を実行する
            subject.set_album("album!")

            # set_tagの引数を検証する
            subject.set_tag.assert_any_call("ALBUM", "album!")

    def test_get_album_artist(self):
        """
        get_album_artist()をテストする。
        """
        # モックを設定する
        with self.init, self.FLAC:

            # テスト対象
            subject = FlacFile("xxx.flac")

            # 戻り値を設定する
            subject.get_tag = MagicMock(return_value="albumartist!")

            # テスト対象を実行する
            self.assertEqual(subject.get_album_artist(), "albumartist!")

            # タグ名を検証する
            subject.get_tag.assert_any_call("ALBUMARTIST")

    def test_set_album_artist(self):
        """
        set_album_artist(album_artist)をテストする。
        """
        # モックを設定する
        with self.init, self.FLAC:

            # テスト対象
            subject = FlacFile("xxx.flac")

            # 戻り値を設定する
            subject.set_tag = MagicMock()

            # テスト対象を実行する
            subject.set_album_artist("albumartist!")

            # set_tagの引数を検証する
            subject.set_tag.assert_any_call("ALBUMARTIST", "albumartist!")

    def test_get_date(self):
        """
        get_date()をテストする。
        """
        # モックを設定する
        with self.init, self.FLAC:

            # テスト対象
            subject = FlacFile("xxx.flac")

            # 戻り値を設定する
            subject.get_tag = MagicMock(return_value="2016-05-04")

            # テスト対象を実行する
            self.assertEqual(subject.get_date(), "2016-05-04")

            # タグ名を検証する
            subject.get_tag.assert_any_call("DATE")

    def test_set_date(self):
        """
        set_date(date)をテストする。
        """
        # モックを設定する
        with self.init, self.FLAC:

            # テスト対象
            subject = FlacFile("xxx.flac")

            # 戻り値を設定する
            subject.set_tag = MagicMock()

            # テスト対象を実行する
            subject.set_date("2016-05-04")

            # set_tagの引数を検証する
            subject.set_tag.assert_any_call("DATE", "2016-05-04")

    def test_get_disc_total(self):
        """
        get_disc_total()をテストする。
        """
        # モックを設定する
        with self.init, self.FLAC:

            # テスト対象
            subject = FlacFile("xxx.flac")

            # 戻り値を設定する
            subject.get_tag = MagicMock(return_value="3")

            # テスト対象を実行する
            self.assertEqual(subject.get_disc_total(), 3)

            # タグ名を検証する
            subject.get_tag.assert_any_call("DISCTOTAL")

    def test_set_disc_total(self):
        """
        set_disc_total(disc_total)をテストする。
        """
        # モックを設定する
        with self.init, self.FLAC:

            # テスト対象
            subject = FlacFile("xxx.flac")

            # 戻り値を設定する
            subject.set_tag = MagicMock()

            # テスト対象を実行する
            subject.set_disc_total(3)

            # set_tagの引数を検証する
            subject.set_tag.assert_any_call("DISCTOTAL", "3")

    def test_get_disc_number(self):
        """
        get_disc_number()をテストする。
        """
        # モックを設定する
        with self.init, self.FLAC:

            # テスト対象
            subject = FlacFile("xxx.flac")

            # 戻り値を設定する
            subject.get_tag = MagicMock(return_value="2")

            # テスト対象を実行する
            self.assertEqual(subject.get_disc_number(), 2)

            # タグ名を検証する
            subject.get_tag.assert_any_call("DISCNUMBER")

    def test_set_disc_number(self):
        """
        set_disc_number(disc_number)をテストする。
        """
        # モックを設定する
        with self.init, self.FLAC:

            # テスト対象
            subject = FlacFile("xxx.flac")

            # 戻り値を設定する
            subject.set_tag = MagicMock()

            # テスト対象を実行する
            subject.set_disc_number(2)

            # set_tagの引数を検証する
            subject.set_tag.assert_any_call("DISCNUMBER", "2")

    def test_get_track_total(self):
        """
        get_track_total()をテストする。
        """
        # モックを設定する
        with self.init, self.FLAC:

            # テスト対象
            subject = FlacFile("xxx.flac")

            # 戻り値を設定する
            subject.get_tag = MagicMock(return_value="15")

            # テスト対象を実行する
            self.assertEqual(subject.get_track_total(), 15)

            # タグ名を検証する
            subject.get_tag.assert_any_call("TRACKTOTAL")

    def test_set_track_total(self):
        """
        set_track_total(track_total)をテストする。
        """
        # モックを設定する
        with self.init, self.FLAC:

            # テスト対象
            subject = FlacFile("xxx.flac")

            # 戻り値を設定する
            subject.set_tag = MagicMock()

            # テスト対象を実行する
            subject.set_track_total(15)

            # set_tagの引数を検証する
            subject.set_tag.assert_any_call("TRACKTOTAL", "15")

    def test_get_track_number(self):
        """
        get_track_number()をテストする。
        """
        # モックを設定する
        with self.init, self.FLAC:

            # テスト対象
            subject = FlacFile("xxx.flac")

            # 戻り値を設定する
            subject.get_tag = MagicMock(return_value="8")

            # テスト対象を実行する
            self.assertEqual(subject.get_track_number(), 8)

            # タグ名を検証する
            subject.get_tag.assert_any_call("TRACKNUMBER")

    def test_set_track_number(self):
        """
        set_track_number(track_number)をテストする。
        """
        # モックを設定する
        with self.init, self.FLAC:

            # テスト対象
            subject = FlacFile("xxx.flac")

            # 戻り値を設定する
            subject.set_tag = MagicMock()

            # テスト対象を実行する
            subject.set_track_number(8)

            # set_tagの引数を検証する
            subject.set_tag.assert_any_call("TRACKNUMBER", "8")

    def test_get_title(self):
        """
        get_title()をテストする。
        """
        # モックを設定する
        with self.init, self.FLAC:

            # テスト対象
            subject = FlacFile("xxx.flac")

            # 戻り値を設定する
            subject.get_tag = MagicMock(return_value="title!")

            # テスト対象を実行する
            self.assertEqual(subject.get_title(), "title!")

            # タグ名を検証する
            subject.get_tag.assert_any_call("TITLE")

    def test_set_title(self):
        """
        set_title(title)をテストする。
        """
        # モックを設定する
        with self.init, self.FLAC:

            # テスト対象
            subject = FlacFile("xxx.flac")

            # 戻り値を設定する
            subject.set_tag = MagicMock()

            # テスト対象を実行する
            subject.set_title("title!")

            # set_tagの引数を検証する
            subject.set_tag.assert_any_call("TITLE", "title!")

    def test_get_artist_list(self):
        """
        get_artist_list()をテストする。
        """
        # モックを設定する
        with self.init, self.FLAC:

            # テスト対象
            subject = FlacFile("xxx.flac")

            # 戻り値を設定する
            subject.get_tags = MagicMock(return_value=["art1", "art2"])

            # テスト対象を実行する
            self.assertEqual(subject.get_artist_list(), ["art1", "art2"])

            # タグ名を検証する
            subject.get_tags.assert_any_call("ARTIST")

    def test_set_artist_list(self):
        """
        set_artist_list(artist_list)をテストする。
        """
        # モックを設定する
        with self.init, self.FLAC:

            # テスト対象
            subject = FlacFile("xxx.flac")

            # 戻り値を設定する
            subject.set_tag = MagicMock()

            # テスト対象を実行する
            subject.set_artist_list(["art1", "art2"])

            # set_tagの引数を検証する
            subject.set_tag.assert_any_call("ARTIST", ["art1", "art2"])

    def test_get_tags(self):
        """
        get_tags(tag)をテストする。
        """
        # モックを設定する
        with self.init, self.FLAC as FLAC:

            # getの戻り値を設定する
            FLAC.return_value.get = MagicMock(return_value=["val1", "val2"])

            # テスト対象
            subject = FlacFile("xxx.flac")

            # テスト対象を実行する
            self.assertEqual(subject.get_tags("tagname"), ["val1", "val2"])

            # getの引数を検証する
            FLAC.return_value.get.assert_any_call("tagname", [])

    def test_get_tag(self):
        """
        get_tag(tag)をテストする。
        指定されたタグの値がある場合、その最初の要素を返すことを確認する。
        """
        # モックを設定する
        with self.init, self.FLAC:

            # テスト対象
            subject = FlacFile("xxx.flac")

            # get_tagsの戻り値を設定する
            subject.get_tags = MagicMock(return_value=["val1", "val2"])

            # テスト対象を実行する
            self.assertEqual(subject.get_tag("tagname"), "val1")

            # getの引数を検証する
            subject.get_tags.assert_any_call("tagname")

    def test_get_tag_without_value(self):
        """
        get_tag(tag)をテストする。
        指定されたタグの値がない場合、Noneを返すことを確認する。
        """
        # モックを設定する
        with self.init, self.FLAC:

            # テスト対象
            subject = FlacFile("xxx.flac")

            # get_tagsの戻り値を設定する
            subject.get_tags = MagicMock(return_value=[])

            # テスト対象を実行する
            self.assertIsNone(subject.get_tag("tagname"))

            # getの引数を検証する
            subject.get_tags.assert_any_call("tagname")

    def test_set_tag(self):
        """
        set_tag(tag, value)をテストする。
        """
        # モックを設定する
        with self.init, self.FLAC as FLAC:

            # テスト対象
            subject = FlacFile("xxx.flac")

            # テスト対象を実行する
            subject.set_tag("tagname", "val1")

            # getの引数を検証する
            FLAC.return_value.__setitem__.assert_any_call("tagname", "val1")

    def test_get_image(self):
        """
        get_image()をテストする。
        """
        # モックを設定する
        with self.init, self.FLAC as FLAC, self.Image as Image:

            # テスト対象
            subject = FlacFile("xxx.flac")

            # FLACが返す画像リストを設定する
            picture = MagicMock(mime="image/png", data="0xFFFF")
            FLAC.return_value.pictures = [picture]

            # 作成されるImageを設定する
            Image.create_from_data.return_value = "<image>"

            # テスト対象を実行する
            self.assertEqual(subject.get_image(), "<image>")

            # Image.create_from_dataの引数を検証する
            Image.create_from_data.assert_any_call("image/png", "0xFFFF")

    def test_get_image_no_picture(self):
        """
        get_image()をテストする。
        画像がない場合、Noneを返すことを確認する。
        """
        # モックを設定する
        with self.init, self.FLAC as FLAC:

            # テスト対象
            subject = FlacFile("xxx.flac")

            # FLACが返す画像リストを設定する
            FLAC.return_value.pictures = []

            # テスト対象を実行する
            self.assertIsNone(subject.get_image())

    def test_set_image(self):
        """
        set_image(image)をテストする。
        """
        # モックを設定する
        with self.init, self.FLAC as FLAC, self.Picture as Picture:

            # テスト対象
            subject = FlacFile("xxx.flac")

            # 引数のImageを設定する
            image = MagicMock()
            image.get_data.return_value = "0xFFFF"

            # テスト対象を実行する
            subject.set_image(image)

            # 画像の設定内容を検証する
            self.assertEqual(Picture.return_value.type, 3)
            self.assertEqual(Picture.return_value.data, "0xFFFF")
            # 画像が追加された
            FLAC.return_value.add_picture.assert_any_call(Picture.return_value)

    def test_update_tags(self):
        """
        update_tags(track_info)をテストする。
        """
        # モックを設定する
        with self.init, self.FLAC as FLAC:

            # テスト対象
            subject = FlacFile("xxx.flac")

            # set_tags_by_track_infoをモック化する
            subject.set_tags_by_track_info = MagicMock()

            # トラック情報のモック
            track_info = MagicMock()

            # テスト対象を実行する
            subject.update_tags(track_info)

            # FLACファイル
            flac_file = FLAC.return_value

            # 既存のタグと画像を削除する
            flac_file.clear.assert_any_call()
            flac_file.clear_pictures.assert_any_call()

            # トラック情報のタグ情報を設定する
            subject.set_tags_by_track_info.assert_any_call(track_info)

            # タグの変更を保存する
            flac_file.save.assert_any_call()

    def test_set_tags_by_track_info(self):
        """
        set_tags_by_track_info(track_info)をテストする。
        """
        # モックを設定する
        with self.init, self.FLAC:

            # テスト対象
            subject = FlacFile("xxx.flac")
            subject.set_album = MagicMock()
            subject.set_album_artist = MagicMock()
            subject.set_date = MagicMock()
            subject.set_image = MagicMock()
            subject.set_disc_total = MagicMock()
            subject.set_disc_number = MagicMock()
            subject.set_track_total = MagicMock()
            subject.set_track_number = MagicMock()
            subject.set_title = MagicMock()
            subject.set_artist_list = MagicMock()

            # トラック情報
            track_info = MagicMock()
            # ディスク情報
            disc_info = track_info.get_disc_info.return_value
            # アルバム情報
            album_info = disc_info.get_album_info.return_value

            album_info.get_album.return_value = "album!"
            album_info.get_album_artist.return_value = "albumartist!"
            album_info.get_date.return_value = "2016-05-04"
            album_info.get_image.return_value = "<image>"
            album_info.get_disc_total.return_value = 3
            disc_info.get_disc_number.return_value = 2
            disc_info.get_track_total.return_value = 15
            track_info.get_track_number.return_value = 8
            track_info.get_title.return_value = "title!"
            track_info.get_artist_list.return_value = ["art1", "art2"]

            # テスト対象を実行する
            subject.set_tags_by_track_info(track_info)

            # 実行結果を検証する
            subject.set_album.assert_any_call("album!")
            subject.set_album_artist.assert_any_call("albumartist!")
            subject.set_date.assert_any_call("2016-05-04")
            subject.set_image.assert_any_call("<image>")
            subject.set_disc_total.assert_any_call(3)
            subject.set_disc_number.assert_any_call(2)
            subject.set_track_total.assert_any_call(15)
            subject.set_track_number.assert_any_call(8)
            subject.set_title.assert_any_call("title!")
            subject.set_artist_list.assert_any_call(["art1", "art2"])

    def test_get_extension(self):
        """
        get_extension()をテストする。
        """
        # モックを設定する
        with self.init, self.FLAC:

            # テスト対象
            subject = FlacFile("xxx.flac")

            # テスト対象を実行する
            self.assertEqual(subject.get_extension(), ".flac")

if __name__ == "__main__":
    unittest.main()
