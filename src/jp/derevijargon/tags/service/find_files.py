import glob
import os

from jp.derevijargon.tags.file_format.dsf.DSFFile import DSFFile
from jp.derevijargon.tags.file_format.errors import UnsupportedAudioFileFormatError
from jp.derevijargon.tags.file_format.flac.FlacFile import FlacFile


AUDIO_FILE_CLASSES = (FlacFile, DSFFile)
"""オーディオファイルクラスリスト"""

ALL_EXTENSIONS = set()
"""
全拡張子セット

対応しているオーディオファイルすべての拡張子のセット。
"""
# オーディオファイルクラスをループする
for an_audio_file_class in AUDIO_FILE_CLASSES:
    # このクラスの対応する拡張子を追加する
    ALL_EXTENSIONS.update(an_audio_file_class.extensions())


def find_files(directory):
    """
    オーディオファイルを検索し、ファイルリストとして返す。
    """

    # ファイルリスト
    file_list = []

    # ファイルをループする
    for a_file_path in glob.glob(os.path.join(directory, "*")):

        # ファイルでなければ処理しない
        if not os.path.isfile(a_file_path):
            continue

        # 対応していない拡張子なら処理しない
        _, extension = os.path.splitext(a_file_path)
        if extension.lower() not in ALL_EXTENSIONS:
            continue

        # このファイルを処理するAudioFileサブクラスを取得する
        audio_file_class = find_audio_file_class(a_file_path)
        # 取得したクラスのインスタンスを作成する
        new_file = audio_file_class(a_file_path)

        # ファイルをリストに追加する
        file_list.append(new_file)

    return file_list



def find_audio_file_class(file_path):
    """
    指定されたオーディオファイルを処理するAudioFileサブクラスを返す。
    該当するクラスがない場合はUnsupportedAudioFileFormatErrorを送出する。
    """

    # オーディオファイルクラスをループする
    for an_audio_file_class in AUDIO_FILE_CLASSES:

        # このクラスでファイルを処理できる場合
        if an_audio_file_class.can_handle(file_path):
            # このクラスを返す
            return an_audio_file_class

    # クラスが見つからなかった場合はエラーとする
    raise UnsupportedAudioFileFormatError(file_path)
