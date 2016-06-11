import os

from jp.derevijargon.tags.meta.AlbumInfo import AlbumInfo
from jp.derevijargon.tags.meta.Image import Image
from jp.derevijargon.tags.tag_file.const import tag_file_name, tag_file_open_options, artist_separator

def read_tag_file(directory):
    """
    指定されたディレクトリのタグファイルを読み込んでアルバム情報を作成する。
    タグファイルがない場合はNoneを返す。
    """

    # ファイルパス
    file_path = os.path.join(directory, tag_file_name)
    # ファイルがなければNoneを返す
    if not os.path.exists(file_path):
        return None
    # ファイルを開く
    with open(file_path, "r", **tag_file_open_options) as file:

        # タグファイルを全行読み込む(末尾の改行を削除)
        lines = [x.rstrip() for x in file]

        # アルバム情報を作成する
        album_info = create_album_info(directory, lines[:3])

        # タグファイルの4行目以降をループする
        for a_line in lines[3:]:

            # 空白行である場合
            if a_line == "":
                # ディスク情報を作成する
                disc_info = album_info.create_disc_info()

            # 空白行ではない場合
            else:
                # タイトルとアーティストリストに分解する
                title, *artist_list = a_line.split(artist_separator)
                # トラック情報を作成する
                disc_info.create_track_info(title, artist_list)

    return album_info


def create_album_info(directory, lines):
    """
    タグファイルの最初の3行からアルバム情報を作成する。
    """

    # アルバム、アルバムアーティスト、発売日
    album, album_artist, date = lines
    # 画像を読み込む
    image = load_image(directory)
    # アルバム情報
    album_info = AlbumInfo(album, album_artist, date, image)

    return album_info


def load_image(directory):
    """
    画像を読み込む。
    """

    # 画像の拡張子をループする
    for an_extension in set(Image.EXTENSION_MAP.values()):
        # 画像のファイルパス
        image_file_path = os.path.join(directory, Image.FILE_NAME + an_extension)
        # このファイルが存在する場合
        if os.path.exists(image_file_path):
            # 画像を作成してループを抜ける
            return Image.create_from_file(image_file_path)

    return None
