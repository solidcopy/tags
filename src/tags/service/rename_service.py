import os

from tags.common import messages
from audio_files.find_files import find_files


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
        right_file_name = determine_file_name(a_file)
        # リネームする
        os.rename(a_file.file_path, os.path.join(directory, right_file_name))

    print(messages.END_RENAME)


def determine_file_name(file):
    """
    タグから適切なファイル名を決定する。
    """

    # ファイル名
    file_name = ""

    # ディスクが複数枚の場合
    if 1 < file.disc_total:
        # ディスク番号を付与する
        file_name += add_zero_paddings(file.disc_number, file.disc_total) + "."

    # トラック番号を付与する
    file_name += add_zero_paddings(file.track_number, file.track_total) + "."

    # タイトルを付与する
    file_name += file.title_as_file_name

    # 拡張子を付与する
    file_name += file.extensions()[0]

    return file_name


def add_zero_paddings(number, max_number):
    """
    引数numberを引数max_numberと同じ桁数になるように0詰めした文字列を返す。
    """

    # 文字数
    digits_length = len(str(max_number))
    # 書式
    digits_format = "%0" + str(digits_length) + "d"
    # フォーマットする
    digits = digits_format % number

    return digits
