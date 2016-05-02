# coding: utf-8

import os

import jp.derevijargon.tags.common.messages as messages
from jp.derevijargon.tags.meta.AlbumInfo import AlbumInfo
from jp.derevijargon.tags.service.find_files import find_files
from jp.derevijargon.tags.tag_file.TagFileWriter import TagFileWriter


def execute(directory):
    """
    エクスポート処理を行う。
    """
    print(messages.BEGIN_EXPORT)

    # ファイルを検索する
    file_list = find_files(directory)

    # 処理するファイルがなければ終了する
    if not file_list:
        print(messages.AUDIO_FILE_NOT_FOUND)

    # ファイルリストからアルバム情報を作成する
    album_info = create_album_info(file_list)

    # タグファイルを開く
    with TagFileWriter.open(os.path.join(directory)) as tag_file:
        # アルバム情報を出力する
        tag_file.write(album_info)

    print(messages.END_EXPORT)

def create_album_info(file_list):
    """
    ファイルリストからアルバム情報を作成する。
    """
    # アルバム情報を作成する
    file = file_list[0]
    album_info = AlbumInfo(album=file.get_album(), album_artist=file.get_album_artist(), date=file.get_date(), image=file.get_image())

    # 前回のディスク情報
    previous_disc_info = None

    # ファイルをループする
    for a_file in file_list:

        # ディスク番号が前回と異なる場合
        if (previous_disc_info is None) or (a_file.get_disc_number() != previous_disc_info.get_disc_number()):
            disc_info = album_info.create_disc_info()

        # トラック情報を作成する
        disc_info.create_track_info(title=a_file.get_title(), artist_list=a_file.get_artist_list())

        # 今回のディスク情報を保存する
        previous_disc_info = disc_info

    return album_info
