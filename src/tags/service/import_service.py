import tags.common.messages as messages
from tags.service.find_files import find_files
from tags.tag_file import read_tag_file


def execute(directory):
    """
    インポート処理を行う。
    """

    print(messages.BEGIN_IMPORT)

    # ファイルを検索する
    file_list = find_files(directory)

    # タグファイルからアルバム情報を読み込む
    album_info = read_tag_file.read_tag_file(directory)

    # トラック情報、ファイルをループする
    for a_track_info, a_file in zip(album_info.all_track_info_list, file_list):
        # タグを更新する
        a_file.update_tags(a_track_info)

    print(messages.END_IMPORT)
