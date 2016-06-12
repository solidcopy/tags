import os
import re
import sys

from jp.derevijargon.tags.common import errors
from jp.derevijargon.tags.service import export_service, import_service, rename_service
import jp.derevijargon.tags.tag_file.const as const


def main():
    """
    エントリポイント。
    """
    # 実行するサービスを選択する
    service_list = select_services(sys.argv)

    # サービスをループする
    for a_service in service_list:
        # サービスを実行する
        a_service(os.curdir)


def select_services(args):
    """
    実行するサービスを選択する。
    """
    # コマンドライン引数でサービスが指定されている場合
    if 1 < len(args):
        # サービス指定を元に実行サービスリストを取得する
        service_functions = select_services_by_arg(args[1])
        return service_functions

    # ファイルを元に実行サービスリストを取得する
    return select_services_by_file()


def select_services_by_arg(service_option):
    """
    コマンドライン引数から実行するサービスを選択する。
    """
    # 不正なサービス指定が含まれている場合は例外を投げる
    if re.search("[^eir]", service_option):
        raise errors.UnknownServiceOptionError(service_option)

    # サービスリスト
    service_list = []

    # サービス指定に応じた関数を選択する

    # エクスポート
    if service_option.find("e") != -1:
        service_list.append(export_service.execute)

    # インポート
    if service_option.find("i") != -1:
        service_list.append(import_service.execute)

    # リネーム
    if service_option.find("r") != -1:
        service_list.append(rename_service.execute)

    return service_list


def select_services_by_file():
    """
    実行するサービスをタグファイルの有無で選択する。
    """
    # タグファイルがあればインポート関数とリネーム関数を選択する
    if os.path.exists(const.tag_file_name):
        return (import_service.execute, rename_service.execute)

    # タグファイルがなければエクスポート関数を選択する
    else:
        return (export_service.execute,)


if __name__ == "__main__":
    main()
