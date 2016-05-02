# coding: utf-8

import os

from jp.derevijargon.tags import messages
from jp.derevijargon.tags.find_files import find_files


def execute(directory):
    """
    リネーム処理を行う。
    """
    print(messages.BEGIN_RENAME)

    # ファイルを検索する
    file_list = find_files(directory)

    # ファイルをループする
    for a_file in file_list:
        # 適切なファイル名を決定する
        right_file_name = a_file.determine_file_name()
        # リネームする
        os.rename(a_file.get_file_path(), os.path.join(directory, right_file_name))

    print(messages.END_RENAME)
