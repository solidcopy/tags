# coding: utf-8

import glob
import os

from jp.derevijargon.tags.meta.Format import Format


def find_files(directory):
    """
    オーディオファイルを検索し、ファイルリストとして返す。
    """
    # ファイルリスト
    file_list = []

    # フォーマットをループする
    for a_format in Format:
        # このフォーマットのファイルをループする
        for a_file in glob.glob(os.path.join(directory, "*." + a_format.value["ext"])):
            # ファイルクラス
            fileClass = a_format.value["fileClass"]
            # ファイルクラスのインスタンスを作成する
            new_file = fileClass(a_file)
            # ファイルをリストに追加する
            file_list.append(new_file)

    return file_list
