# coding: utf-8

import jp.derevijargon.tags.common.messages as messages
from jp.derevijargon.tags.service.find_files import find_files
from jp.derevijargon.tags.tag_file.TagFileReader import TagFileReader


def execute(directory):
    """
    インポート処理を行う。
    """
    print(messages.BEGIN_IMPORT)

    # ファイルを検索する
    file_list = find_files(directory)

    # タグファイルからアルバム情報を読み込む
    with TagFileReader.open(directory) as tag_file:
        album_info = tag_file.read()

    # このアルバム情報の全トラック情報リスト
    track_info_list = album_info.get_all_track_info_list()

    # トラック情報、ファイルをループする
    for a_track_info, a_file in zip(track_info_list, file_list):
        # タグを更新する
        a_file.update_tags(a_track_info)

    print(messages.END_IMPORT)
