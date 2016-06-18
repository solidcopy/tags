import tags.common.messages as messages
from tags.meta.AlbumInfo import AlbumInfo
from audio_files.find_files import find_files
from tags.tag_file import write_tag_file


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
        return

    # ファイルリストからアルバム情報を作成する
    album_info = create_album_info(file_list)

    # タグファイルを出力する
    write_tag_file.write_tag_file(directory, album_info)

    print(messages.END_EXPORT)


def create_album_info(file_list):
    """
    ファイルリストからアルバム情報を作成する。
    """

    # アルバム情報を作成する
    file = file_list[0]
    album_info = AlbumInfo(album=file.album, album_artist=file.album_artist, date=file.date, image=file.image)

    # 前回のファイル
    previous_file = None

    # ファイルをループする
    for a_file in file_list:

        # ディスク番号が前回と異なる場合
        if (previous_file is None) or (a_file.disc_number != previous_file.disc_number):
            disc_info = album_info.create_disc_info()

        # トラック情報を作成する
        disc_info.create_track_info(title=a_file.title, artist_list=a_file.artist_list)

        # 今回のディスク情報を保存する
        previous_file = a_file

    return album_info
