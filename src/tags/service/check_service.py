import os
import unicodedata
from pathlib import Path

import tags.common.messages as messages


def execute(directory):
    """
    チェック処理を行う。
    """

    print(messages.BEGIN_CHECK)

    # tagsファイルを検索する
    tags_files = find_tags_files(directory)

    # tagsファイルにNFDが含まれているかチェックする
    nfd_occurences = detect_nfd_occurences_in_files(tags_files)

    # tagsファイルのチェック結果を表示する
    show_nfd_occurences_in_tags_files(nfd_occurences)

    if nfd_occurences:
        print(messages.ASK_CONVERT_TO_NFC)
        while True:
            answer = input()
            if answer.lower() == 'y':
                rewrite_to_nfc(nfd_occurences.keys())
                break
            elif answer.lower() == 'n':
                break

    print(messages.END_CHECK)

def find_tags_files(directory):
    """
    tagsファイルを検索する。

    :param directory: ディレクトリ
    :return: tagsファイルパスのリスト
    """

    tags_files = []

    for directory, _, files in os.walk(directory):

        directory = Path(directory).absolute()

        if 'tags' in files:
            tags_file = Path(directory, 'tags')
            tags_files.append(tags_file)

    return tags_files

def detect_nfd_occurences_in_files(tags_files):
    """
    tagsファイルにNFDが含まれているかチェックする。

    :param tags_files: tagsファイルパスのリスト
    :return: NFD出現箇所リスト
    """

    nfd_occurences = {}

    for tags_file in tags_files:
        new_nfd_occurences = detect_nfd_occurences_in_file(tags_file)

        if len(new_nfd_occurences) > 0:

            nfd_occurences[tags_file] = new_nfd_occurences

    return nfd_occurences

def detect_nfd_occurences_in_file(tags_file):
    """
    tagsファイルにNFDが含まれているかチェックする。

    :param tags_file: tagsファイルパスのリスト
    :return: NFD出現箇所リスト
    """

    nfd_occurences = []

    with open(tags_file) as tags_file_in:
        for line_number, line in enumerate(tags_file_in.readlines(), 1):
            line = line.rstrip()

            if line != unicodedata.normalize('NFC', line):

                nfd_occurences.append([line_number, line])

    return nfd_occurences

def show_nfd_occurences_in_tags_files(nfd_occurences):
    """
    tagsファイルのチェック結果を表示する。

    :param nfd_occurences: NFD出現箇所
    :return:
    """

    if len(nfd_occurences) == 0:
        print(messages.NO_NFD_DETECTED_IN_TAGS)
        return

    print(messages.NFD_DETECTED_IN_TAGS)

    for tags_file in sorted(nfd_occurences.keys()):

        for line_number, line in nfd_occurences[tags_file]:

            print(f"{tags_file}:{line_number}")
            print(f"    {line}")

def rewrite_to_nfc(tags_files):
    """
    tagsファイルの内容をNFCに変換する。

    :param tags_files: tagsファイルパスのリスト
    :return:
    """

    for tags_file in tags_files:

        tags_file_content = None
        with open(tags_file, encoding="utf-8") as tags_file_in:
            tags_file_content = tags_file_in.read()

        tags_file_content = unicodedata.normalize('NFC', tags_file_content)

        with open(tags_file, 'w', encoding="utf-8") as tags_file_out:
            tags_file_out.write(tags_file_content)

        print(messages.REWRITE_COMPLETED % tags_file)
