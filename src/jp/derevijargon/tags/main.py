# coding: utf-8

import os
import sys

'''
エントリポイント。
'''
def main():
    service = select_service(sys.argv)
    service(os.curdir)


import os
import sys
from const import *
from messages import *

'''
実行するサービスを選択する。
'''
def select_service(args):
    # コマンドライン引数が指定されている場合
    if 1 < len(args):
        # サービス指定
        service_option = args[1]

        # サービス指定に応じた関数を選択する
        if service_option == 'e':
            from export_service import execute
        elif service_option == 'i':
            from import_service import execute
        elif service_option == 'r':
            from rename_service import execute
        else:
            print(MSG_UNKNOWN_SERVICE % service_option)
            sys.exit(1)

        return execute

    # タグファイルがあればインポート関数を選択する
    if os.path.exists(tag_file_name):
        from import_service import execute
    # タグファイルがなければエクスポート関数を選択する
    else:
        from export_service import execute

    return execute

if __name__ == '__main__':
    main()