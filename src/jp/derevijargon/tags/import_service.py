# coding: utf-8

import collections
import os
import sys

from jp.derevijargon.tags.Image import Image
from jp.derevijargon.tags.const import *
from jp.derevijargon.tags.find_files import find_files
from jp.derevijargon.tags.messages import *
from jp.derevijargon.tags.read_tag_file import read_tag_file


def execute(directory):
    """
    インポート処理を行う。
    """

    print(MSG_START_IMPORT)

    # ファイルを検索する
    file_list = find_files(directory)

    # 処理するファイルがなければ終了する
    if not file_list:
        print(MSG_NO_AUDIO_FILE_FOUND)
        sys.exit(0)

    # タグファイルがなければ終了する
    tag_file_path = os.path.join(directory, tag_file_name)
    if not os.path.exists(tag_file_path):
        print(MSG_TAG_FILE_NOT_FOUND)
        sys.exit(1)

    # タグファイルを読み込む
    album_info = read_tag_file(tag_file_path)

    # トラック情報とファイルの数が一致しなければ終了する
    if album_info.get_number_of_track_infos() != len(file_list):
        print(MSG_NUMBER_OF_TRACKS_UNMATCHED % (album_info.get_number_of_track_infos(), len(file_list)))
        sys.exit(1)

    # 画像
    image = None
    # 画像の拡張子をループする
    for an_extension in image_extensions.values():
        # 画像のファイルパス
        image_file_path = os.path.join(directory, image_file_name + "." + an_extension)
        # このファイルが存在する場合
        if os.path.exists(image_file_path):
            # 画像を作成してループを抜ける
            image = Image.create_from_file(image_file_path)
            break

    # ファイルのインデックス
    file_index = 0
    # ディスク情報をループする
    for a_disc_info in album_info.get_disc_info_list():
        # トラック情報をループする
        for a_track_info in a_disc_info.get_track_info_list():
            # ファイル
            file = file_list[file_index]
            file_index += 1
            # タグを更新する
            file.update(collections.ChainMap(album_info.tags, a_disc_info.tags, a_track_info))
            # 不要タグを削除する
            file.remove_tags(removed_tags)

            # 画像を削除する
            file.remove_images()
            # 画像がある場合は設定する
            if image is not None:
                file.set_image(image)

            # 変更を保存する
            file.save()

    print(MSG_END_IMPORT)
