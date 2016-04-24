# coding: utf-8

import os

from jp.derevijargon.tags.const import *
from jp.derevijargon.tags.find_files import find_files
from jp.derevijargon.tags.messages import *


def execute(directory):
    """
    リネーム処理を行う。
    """

    print(MSG_START_RENAME)

    # ファイルを検索する
    file_list = find_files(directory)

    # 処理するファイルがなければ終了する
    if not file_list:
        print(MSG_NO_AUDIO_FILE_FOUND)

    # ファイルをループする
    for a_file in file_list:
        # 適切なファイル名を決定する
        right_file_name = determine_file_name(a_file)
        # 現在のファイル名
        current_file_name = os.path.split(a_file.get_file_path())[-1]
        # ファイル名が適切でない場合
        if current_file_name != right_file_name:
            # リネームする
            os.rename(a_file.get_file_path(), os.path.join(os.path.dirname(a_file.get_file_path()), right_file_name))

    print(MSG_END_RENAME)

def determine_file_name(file):
    """
    タグから適切なファイル名を決定する。
    """

    # ファイル名
    file_name = ""

    # ディスクが複数枚の場合
    if file.get_tag(tag_disc_total) != "1":
        # ディスク番号の桁数
        disc_number_length = len(file.get_tag(tag_disc_total))
        # ディスク番号
        disc_number = ("%0" + str(disc_number_length) + "d") % int(file.get_tag(tag_disc_number))
        # ディスク番号を付与する
        file_name += disc_number + "."

    # トラック番号の桁数
    track_number_length = len(file.get_tag(tag_track_total))
    # トラック番号
    track_number = ("%0" + str(track_number_length) + "d") % int(file.get_tag(tag_track_number))
    # トラック番号を付与する
    file_name += track_number + "."

    # タイトルのファイル名に使用できない文字を代替文字に置換する
    title = file.get_tag(tag_title)
    for src, dest in replace_char_list:
        title = title.replace(src, dest)

    # タイトルを付与する
    file_name += title

    # 拡張子を付与する
    file_name += os.path.splitext(file.get_file_path())[-1]

    return file_name
