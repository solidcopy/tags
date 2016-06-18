import os

from tags.tag_file.const import tag_file_name, artist_separator, tag_file_open_options


def write_tag_file(directory, album_info):
    """
    タグファイルを出力する。
    """

    # ファイルパス
    file_path = os.path.join(directory, tag_file_name)
    # ファイルを開く
    with open(file_path, "w", **tag_file_open_options) as file:

        # アルバム情報を出力する
        write_album_info(file, album_info)

        # ディスク情報をループする
        for a_disc_info in album_info.disc_info_list:
            # 空白行を出力する
            file.write("\n")

            # トラック情報をループする
            for a_track_info in a_disc_info.track_info_list:
                # トラック情報を出力する
                write_track_info(file, album_info, a_track_info)

        # 画像がある場合
        image = album_info.image
        if image is not None:
            # 画像をファイルに保存する
            write_image(directory, image)


def write_album_info(file, album_info):
    """
    アルバム情報を出力する。
    """

    # アルバム名
    file.write(album_info.album or "")
    file.write("\n")
    # アルバムアーティスト
    file.write(album_info.album_artist or "")
    file.write("\n")
    # 発売日
    file.write(album_info.date or "")
    file.write("\n")


def write_track_info(file, album_info, track_info):
    """
    トラック情報を出力する。
    """

    # タイトルを出力する
    file.write(track_info.title or "")

    # アーティストがアルバムアーティストと異なる場合
    if track_info.artist_list != [album_info.album_artist]:
        # アーティストをループする
        for an_artist in track_info.artist_list:
            # 区切りを出力する
            file.write(artist_separator)
            # アーティストを出力する
            file.write(an_artist)

    # 改行を出力する
    file.write("\n")


def write_image(directory, image):
    """
    画像をファイルに保存する。
    """

    # ファイルを開く
    with open(os.path.join(directory, image.file_name), "wb") as image_file:
        # 画像を出力する
        image_file.write(image.data)
