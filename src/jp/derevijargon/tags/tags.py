# coding: utf-8

# オーディオファイルのタグ情報を管理するバッチ。
#
# カレントディレクトリとそのサブディレクトリ群を順次処理する。
# ディレクトリにこのプログラムの処理対象となるオーディオファイルが1つもなければ無視する。
# ディレクトリにtagsというファイルがあればインポート処理、なければエクスポート処理を行う。
#
# インポート処理では、tagsの内容通りにオーディオファイルのタグ情報を更新する。
# オーディオファイルのファイル名をトラック番号とタイトルから決定し、
# その時のファイル名と一致しなければリネームする。
#
# エクスポート処理ではオーディオファイルのタグ情報をtagsに出力する。

#結論としては、インポート処理の一環としてオーディオファイルのリネームを行う。
#タグファイルの中ではファイル名は保持せずにファイル名昇順でソートした順序でファイルを識別する。

import os

from const import *
from AudioFile import AudioFile
from FlacFile import FlacFile
from UnsupportedFormatError import UnsupportedFormatError

'''
tagsを実行する。
'''
def execute():

    # カレントディレクトリ配下をループする
    for (root, dirs, files) in os.walk(os.curdir):

        # ファイルリストから処理対象のファイルではないものを除外する
        filtered_files = filter_files(files)

        # 対象ファイルがなければこのディレクトリは処理しない
        if len(filtered_files) == 0:
            continue

        # ファイルをオーディオファイルに変換する
        audio_files = convert_to_audio_files(root, filtered_files)

        # タグファイルがなければエクスポート処理を開始する
        if files.count(tag_file) == 0:
            export_tags(root, audio_files)

        # タグファイルがあればインポート処理を開始する
        else:
            import_tags(root, audio_files)

'''
ファイルリストから処理対象のファイルではないものを除外する。
'''
def filter_files(files):

    # フィルター後のファイルリスト
    filtered_files = []

    # ファイルをループする
    for file in files:
        # 処理対象のファイルである場合
        if filter_file(file):
            # リストに追加する
            filtered_files.append(file)

    return filtered_files

'''
処理対象のファイルであるかを返す。
'''
def filter_file(file):

    # 拡張子を取得する
    ext = os.path.splitext(file)[1]

    # 拡張子が処理対象ファイルのものであるかを返す
    return (0 < target_exts.count(ext))

'''
リストの各要素をオーディオファイルに変換する。
'''
def convert_to_audio_files(directory, filtered_files):

    # オーディオファイルリスト
    audio_files = []

    # ファイルをループする
    for file in filtered_files:
        # フルパスに変換する
        path = os.path.join(directory, file)
        # オーディオファイルに変換する
        audio_file = convert_to_audio_file(path)
        # リストに追加する
        audio_files.append(audio_file)

    return audio_files

'''
ファイルをオーディオファイルに変換する。
'''
def convert_to_audio_file(file):

    # 拡張子を取得する
    ext = os.path.splitext(file)[1]

    # 拡張子に応じたオブジェクトに変換する
    # FLAC
    if ext == '.flac':
        return FlacFile(file)

    # 上記以外の場合
    else:
        raise UnsupportedFormatError(ext)

'''
エクスポート処理を行う。
'''
def export_tags(directory, audio_files):

    # タグ情報を取得する
    tags = get_tags(audio_files)

    # タグファイルを出力する
    write_tag_file(directory, tags)

    # 画像を出力する
    write_image(directory, audio_files[0])

'''
タグ情報を取得する。

取得したタグ情報はリストとなり、各要素がファイルごとのタグ情報を保持する。
ファイルごとのタグ情報はタグ名から値への辞書である。

リストの先頭要素はアルバムタグの辞書となる。
これは引数の最初のファイルから取得され、リストのファイル間に不一致があっても警告しない。
'''
def get_tags(audio_files):

    # タグ情報
    tags = []

    # 最初のファイルであるか
    first_file = True

    # オーディオファイルをループする
    for audio_file in audio_files:

        # 最初のファイルである場合
        if first_file:
            # アルバムタグを取得する
            album_tags = audio_file.get_album_tags()
            tags.append(album_tags)
            # 次からは最初のファイルではない
            first_file = False

        # トラックタグを取得する
        track_tags = audio_file.get_track_tags()
        tags.append(track_tags)

    return tags

'''
タグファイルを出力する。
'''
def write_tag_file(directory, tags):

    # タグファイルを開く
    with open(os.path.join(directory, tag_file), 'w', encoding=tag_file_encoding) as file:

        # アルバムタグ情報
        album_tag_info = tags[0]

        # アルバムタグをループする
        for tag in album_tags:

            # ファイルに出力する
            file.write(tag + '=' + album_tag_info[tag] + '\n')

        # トラックタグ情報をループする
        for tag_info in tags[1:]:

            # 改行を出力する
            file.write('\n')

            # トラックタグをループする
            for tag in track_tags:

                # ファイルに出力する
                file.write(tag + '=' + tag_info[tag] + '\n')

'''
画像を出力する。
'''
def write_image(directory, audio_file):

    # 拡張子
    ext = audio_file.get_image_ext()

    # 画像がない場合は終了する
    if not ext:
        return

    # ファイル名
    image_file = os.path.join(directory, 'Folder.' + ext)

    # 画像ファイルを出力する
    with open(image_file, 'wb') as file:
        file.write(audio_file.get_image_data())

'''
インポート処理を行う。
'''
def import_tags(directory, audio_files):

    # タグファイルからタグ情報を読み込む
    tags = parse_tag_file(directory)

    # アルバムタグ情報
    album_tag_info = tags[0]
    # トラックタグ情報リスト
    track_tag_infos = tags[1:]

    # トラックタグ情報とファイルの件数が一致しなければ処理しない
    if len(track_tag_infos) != len(audio_files):
        print('トラックタグ情報とファイルの件数が一致しません。')
        return

    # 画像を読み込む
    new_image_data = read_image(directory)

    # トラックタグ情報の件数分ループする
    for i in range(0, len(track_tag_infos)):
        track_tag_info = track_tag_infos[i]
        audio_file = audio_files[i]

        # タグ情報をマージする
        tag_info = album_tag_info.copy()
        tag_info.update(track_tag_info)

        # このファイルを更新したか
        modified = False

        # タグをループする
        for tag in all_tags:
            # 設定する値を取得する
            new_value = tag_info[tag]

            # 設定されている値を取得する
            old_value = audio_file.get_tag(tag)

            # 変更する必要がなければこのタグは処理しない
            if old_value == new_value:
                continue

            # 既存のタグを削除する
            audio_file.remove_tag(tag)
            # 新しいタグを設定する
            audio_file.set_tag(tag, new_value)
            # ファイルを更新した
            modified = True

        # 既存の画像を取得する
        old_image_data = audio_file.get_image_data()

        # 画像を変更する必要がある場合
        if old_image_data != new_image_data:
            # 画像を設定する
            audio_file.set_image(new_image_data)
            # ファイルを更新した
            modified = True

        # ファイルを更新した場合
        if modified:
            # 更新を保存する
            audio_file.save()

        # ファイル名をリネームする
        audio_file.rename_file()

'''
タグファイルからタグ情報を読み込む。
'''
def parse_tag_file(directory):

    # タグファイルのパス
    tag_file_path = os.path.join(directory, tag_file)

    # タグ情報
    tags = []

    # 次のタグは新しい辞書に追加するべきか
    new_dict = True

    # タグファイルを開く
    with open(tag_file_path, 'r', encoding=tag_file_encoding) as file:

        # 行をループする
        for line in file.readlines():
            line = line.rstrip()

            # 空白行である場合
            if line == '':
                # 次のタグは新しい辞書に追加する
                new_dict = True
                continue

            # 新しい辞書を作るべきならそうする
            if new_dict:
                tag_dict = {}
                tags.append(tag_dict)
                # 次のタグは同じ辞書に追加する
                new_dict = False

            # 行をタグと値に分割する
            tag, value = line.split('=')

            # 辞書に追加する
            tag_dict[tag] = value

    return tags

'''
画像を読み込む。
'''
def read_image(directory):

    # 画像のパス
    image_path = find_image(directory)

    if image_path is None:
        return None

    with open(image_path, 'rb') as file:
        return file.read()

'''
画像ファイルのパスを返す。
'''
def find_image(directory):
    for image_file in image_files:
        image_path = os.path.join(directory, image_file)
        if os.path.exists(image_path):
            return image_path
    return None

if __name__ == '__main__':
    execute()
