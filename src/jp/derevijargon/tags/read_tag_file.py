# coding: utf-8

import re

from jp.derevijargon.tags.AlbumInfo import AlbumInfo
from jp.derevijargon.tags.DiscInfo import DiscInfo
from jp.derevijargon.tags.const import *


def read_tag_file(tag_file_path):
    '''
    タグファイルを読み込む。
    '''

    # アルバム情報を作成する
    album_info = AlbumInfo()

    # タグファイルを開く
    with open(tag_file_path, 'r', **tag_file_options) as tag_file:

        # 編集中のディスク情報
        disc_info = None
        # アルバム情報の収集中とする
        reading_tracks = False
        # 次のトラック情報は新しいディスク情報に設定するか
        new_disc = False

        # タグファイルの行をループする
        for a_line in tag_file.readlines():

            # 改行を削除する
            a_line = a_line.rstrip('\n')

            # 空白行である場合
            if not a_line:
                # トラック情報の収集中とする
                reading_tracks = True
                # 次のトラック情報は新しいディスク情報に設定する
                new_disc = True

            # アルバム情報の収集中である場合
            elif not reading_tracks:
                # タグと値を読み込む
                tag, value = parse_album_tag(a_line)
                album_info.tags[tag] = value

            # トラック情報の収集中である場合
            else:
                # 新しいディスク情報を作成すべきである場合
                if new_disc:
                    # ディスク情報を作成する
                    disc_info = DiscInfo()
                    album_info.add_disc_info(disc_info)
                    # 次のトラック情報は新しいディスク情報に設定しない
                    new_disc = False
                # トラック情報を作成する
                track_info = {}
                disc_info.add_track_info(track_info)
                # タイトルとアーティストを読み込む
                title, artists = parse_track_tag(a_line)
                # アーティストがなければアルバムアーティストを設定する
                if artists[0] is None:
                    artists = [album_info.tags[tag_album_artist]]
                # トラック情報にタグを設定する
                track_info[tag_title] = title
                track_info[tag_artist] = artists

    return album_info

def parse_album_tag(line):
    '''
    行をアルバムタグと値に分割して返す。
    タグと値でなければ('', '')。
    '''

    match = re.match('(\\w+)=(.*)', line)
    return match.groups() if match else ('', '')

def parse_track_tag(line):
    '''
    行をタイトルとアーティストに分割して返す。
    アーティストがアルバムアーティストと同じならNone。
    '''
    tag_and_values = line.split(track_info_separator)
    if len(tag_and_values) == 1:
        tag_and_values.append(None)

    return tag_and_values[0], tag_and_values[1:]
