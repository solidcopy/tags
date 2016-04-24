# coding: utf-8

import os

from const import *
from messages import *
from find_files import find_files

'''
エクスポート処理を行う。
'''
def execute(directory):

    print(MSG_START_EXPORT)

    # ファイルを検索する
    file_list = find_files(directory)

    # 処理するファイルがなければ終了する
    if not file_list:
        print(MSG_NO_AUDIO_FILE_FOUND)

    # タグファイルを開く
    with open(os.path.join(directory, tag_file_name), 'w', **tag_file_options) as tag_file:
        # アルバム情報
        album_tags = file_list[0].get_tag_file_album_tags()

        # タグファイルのアルバムタグをループする
        for tag in tag_file_album_tags:
            # タグと値を出力する
            tag_file.write(tag + '=' + album_tags[tag] + '\n')

        # 前回のディスク番号
        last_disc_number = None

        # ファイルをループする
        for a_file in file_list:
            # ディスク情報
            disc_number = a_file.get_tag(tag_disc_number)
            # ディスク番号が前回と異なる場合
            if disc_number != last_disc_number:
                # 空白行を出力する
                tag_file.write('\n')
                # 今回のディスク番号を保存する
                last_disc_number = disc_number

            # トラック情報を出力する
            track_tags = a_file.get_track_tags()
            if album_tags[tag_album_artist] != track_tags[tag_artist]:
                tag_file.write('%s%s%s\n' % (track_tags[tag_title], track_info_separator, track_tags[tag_artist]))
            else:
                tag_file.write(track_tags[tag_title] + '\n')

    # 画像がある場合
    image = file_list[0].get_image()
    if image is not None:
        # 画像をファイルに保存する
        with open(os.path.join(directory, image_file_name + '.' + image.get_extension()), 'wb') as file:
            file.write(image.get_data())

    print(MSG_END_EXPORT)
