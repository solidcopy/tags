# coding: utf-8

import os
import sys
import unittest
from unittest.mock import MagicMock, patch

from jp.derevijargon.tags.common.errors import UnknownServiceOptionError
import jp.derevijargon.tags.main as main
from jp.derevijargon.tags.service import export_service, import_service, rename_service


class Test(unittest.TestCase):
    """
    mainモジュールのテストケース。
    """
    def test_main(self):
        """
        main()をテストする。
        """
        # select_servicesメソッドをモック化する
        with patch("jp.derevijargon.tags.main.select_services") as select_services:
            # 戻り値を設定する
            select_services.return_value = [MagicMock(), MagicMock()]

            # コマンドライン引数を設定する
            sys.argv = ['eir']

            # カレントディレクトリを設定する
            os.curdir = "/root/dir/dir"

            # テスト対象を実行する
            main.main()

            # 実行結果を検証する
            select_services.assert_any_call(sys.argv)
            select_services.return_value[0].assert_any_call(os.curdir)
            select_services.return_value[1].assert_any_call(os.curdir)

    def test_select_services_with_service_option(self):
        """
        select_services(args)をテストする。
        サービス指定がある場合、サービス指定を元にサービスが選択されることを確認する。
        """
        # select_services_by_argメソッドをモック化する
        with patch("jp.derevijargon.tags.main.select_services_by_arg") as select_services_by_arg:
            # 戻り値を設定する
            select_services_by_arg.return_value = ['service1', 'service2']

            # テスト対象を実行する
            returned_value = main.select_services(["", "ir"])
            self.assertSequenceEqual(returned_value, ['service1', 'service2'])

    def test_select_services_without_service_option(self):
        """
        select_services(args)をテストする。
        サービス指定がない場合、タグファイルの有無を元にサービスが選択されることを確認する。
        """
        # select_services_by_fileメソッドをモック化する
        with patch("jp.derevijargon.tags.main.select_services_by_file") as select_services_by_file:
            # 戻り値を設定する
            select_services_by_file.return_value = ['service1', 'service2']

            # テスト対象を実行する
            returned_value = main.select_services([""])
            self.assertSequenceEqual(returned_value, ['service1', 'service2'])

    def test_select_services_by_arg(self):
        """
        select_services_by_arg(service_option)をテストする。
        """
        # エクスポートのみ
        returned_value = main.select_services_by_arg("e")
        self.assertSequenceEqual(returned_value, (export_service.execute,))

        # インポートのみ
        returned_value = main.select_services_by_arg("i")
        self.assertSequenceEqual(returned_value, (import_service.execute,))

        # リネームのみ
        returned_value = main.select_services_by_arg("r")
        self.assertSequenceEqual(returned_value, (rename_service.execute,))

        # インポートおよびリネーム
        returned_value = main.select_services_by_arg("ir")
        self.assertSequenceEqual(returned_value, (import_service.execute, rename_service.execute))

    def test_select_services_by_arg_unknown_service(self):
        """
        select_services_by_arg(service_option)をテストする。
        不正なサービス指定がある場合、UnknownServiceOptionErrorが発生することを確認する。
        """
        try:
            main.select_services_by_arg("ex")
        except UnknownServiceOptionError as e:
            self.assertEqual(str(e), "不正なサービス指定です。ex")

    def test_select_services_by_file_with_tag_file(self):
        """
        select_services_by_file()をテストする。
        タグファイルがある場合、インポートとリネームが選択されることを確認する。
        """
        with patch("os.path") as path:
            path.exists = MagicMock()
            path.exists.return_value = True

            # テスト対象を実行する
            returned_value = main.select_services_by_file()

            # 実行結果を検証する
            self.assertSequenceEqual(returned_value, (import_service.execute, rename_service.execute))

            # カレントディレクトリにタグファイルがあるか確認されている
            path.exists.assert_any_call("tags")

    def test_select_services_by_file_without_tag_file(self):
        """
        select_services_by_file()をテストする。
        タグファイルがない場合、エクスポートが選択されることを確認する。
        """
        with patch("os.path") as path:
            path.exists = MagicMock()
            path.exists.return_value = False

            # テスト対象を実行する
            returned_value = main.select_services_by_file()

            # 実行結果を検証する
            self.assertSequenceEqual(returned_value, (export_service.execute,))

            # カレントディレクトリにタグファイルがあるか確認されている
            path.exists.assert_any_call("tags")

if __name__ == "__main__":
    unittest.main()
