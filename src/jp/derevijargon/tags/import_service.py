# coding: utf-8

from jp.derevijargon.tags.TagFileReader import TagFileReader
from jp.derevijargon.tags.find_files import find_files
import jp.derevijargon.tags.messages as messages


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
