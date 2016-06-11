import os

from mutagen.id3 import ID3

from jp.derevijargon.tags.common import utils
from jp.derevijargon.tags.file_format.errors import AudioFileFormatError
from jp.derevijargon.tags.file_format.id3v2.ID3AudioFile import ID3AudioFile


class DSFFile(ID3AudioFile):
    """
    DSFファイル
    """

    @classmethod
    def extensions(cls):
        """
        拡張子のタプルを返す。
        """

        return (".dsf",)


    def __init__(self, file_path):
        """
        コンストラクタ。
        """

        self.total_file_size_position = None
        """合計ファイルサイズの位置"""
        self.pointer_to_metadata_chunk_position = None
        """メタ情報チャンクポインタの位置"""
        self.pointer_to_metadata_chunk = 0
        """メタ情報チャンクポインタ"""

        super().__init__(file_path)


    def init_tags(self, file_path):
        """
        DSFファイルからメタ情報を読み込む。
        """

        with open(file_path, "rb") as file:
            # DSDチャンクを読み込む
            self.read_dsd_chunk(file, file_path)
            # fmtチャンクを読み込む
            self.read_fmt_chunk(file, file_path)
            # データチャンクを読み込む
            self.read_data_chunk(file, file_path)
            # タグ情報を読み込む
            self.read_tags(file)


    def read_dsd_chunk(self, file, file_path):
        """
        DSDチャンクを読み込む。
        """

        # DSDチャンクヘッダー
        dsd_chunk_header = file.read(4)
        if dsd_chunk_header != b"DSD ":
            raise AudioFileFormatError(file_path, "dsf", "DSDチャンクヘッダーがありません。")

        # このチャンクのサイズ
        dsd_chunk_size = utils.read_long(file)
        if dsd_chunk_size != 28:
            raise AudioFileFormatError(file_path, "dsf", "DSDチャンクのサイズが28ではありません。")

        # ファイルサイズ(読み捨てる)
        self.total_file_size_position = file.tell()
        utils.read_long(file)

        # メタ情報の位置
        self.pointer_to_metadata_chunk_position = file.tell()
        self.pointer_to_metadata_chunk = utils.read_long(file)


    def read_fmt_chunk(self, file, file_path):
        """
        fmtチャンクを読み込む。
        """

        # fmtチャンクヘッダー
        fmt_chunk_header = file.read(4)
        if fmt_chunk_header != b"fmt ":
            raise AudioFileFormatError(file_path, "dsf", "fmtチャンクヘッダーがありません。")

        # このチャンクのサイズ(読み捨てる)
        utils.read_long(file)

        # バージョン
        format_version = utils.read_int(file)
        if format_version != 1:
            raise AudioFileFormatError(file_path, "dsf", "バージョンが1ではありません。")

        # フォーマットID
        format_id = utils.read_int(file)
        if format_id != 0:
            raise AudioFileFormatError(file_path, "dsf", "フォーマットIDが0ではありません。")

        # チャンネルタイプ(1～7)
        channel_type = utils.read_int(file)
        if range(1, 7 + 1).count(channel_type) == 0:
            raise AudioFileFormatError(file_path, "dsf", "チャンネルタイプが0～7ではありません。")

        # チャンネル番号(1～6)
        channel_num = utils.read_int(file)
        if range(1, 6 + 1).count(channel_num) == 0:
            raise AudioFileFormatError(file_path, "dsf", "チャンネル番号が1～6ではありません。")

        # サンプリング周波数(読み捨てる)
        utils.read_int(file)

        # サンプルサイズ(1, 8)
        sample_size = utils.read_int(file)
        if sample_size not in (1, 8):
            raise AudioFileFormatError(file_path, "dsf", "サンプルサイズが1または8ではありません。")

        # サンプル数(読み捨てる)
        utils.read_long(file)

        # チャンネルごとのブロックサイズ
        channel_block_size = utils.read_int(file)
        if channel_block_size != 4096:
            raise AudioFileFormatError(file_path, "dsf", "チャンネルごとのブロックサイズが4096ではありません。")

        # 予備領域
        reserved = file.read(4)
        if reserved != b"\x00" * 4:
            raise AudioFileFormatError(file_path, "dsf", "予備領域がありません。")


    def read_data_chunk(self, file, file_path):
        """
        データチャンクを読み込む。
        """

        # データチャンクヘッダー
        data_chunk_header = file.read(4)
        if data_chunk_header != b"data":
            raise AudioFileFormatError(file_path, "dsf", "データチャンクヘッダーがありません。")

        # このチャンクのサイズ(読み捨てる)
        utils.read_long(file)


    def read_tags(self, file):
        """
        タグ情報を読み込む。
        """

        # タグ情報がない場合は終了する
        if self.pointer_to_metadata_chunk == 0:
            return

        # タグ情報の位置まで読み込み位置を進める
        file.seek(self.pointer_to_metadata_chunk)

        # メタ情報ファイルのパス
        meta_file_path = self.file_path + ".meta"

        try:
            # タグ情報をメタ情報ファイルに出力する
            with open(meta_file_path, "wb") as meta_file:
                metadata = file.read()
                meta_file.write(metadata)

            # mutagenで入出力を可能にする
            id3 = ID3(meta_file_path)
            # ID3の内容でこのファイルのプロパティを初期化する
            self.init_by_id3(id3)

        # メタ情報ファイルを削除する
        finally:
            if os.path.exists(meta_file_path):
                os.remove(meta_file_path)


    def update_file(self):
        """
        このファイルオブジェクトの内容でオーディオファイルのメタ情報を更新する。
        """

        # メタ情報チャンクの位置を決定する
        new_pointer_to_metadata_chunk = self.determine_pointer_to_metadata_chunk()

        # オーディオファイルを開く
        with open(self.file_path, "r+b") as file:

            # メタ情報チャンクの位置を出力する
            file.seek(self.pointer_to_metadata_chunk_position)
            file.write(new_pointer_to_metadata_chunk.to_bytes(8, "little"))

            # 既存のメタ情報がある場合
            if 0 < self.pointer_to_metadata_chunk:
                # メタ情報を削除する
                file.seek(self.pointer_to_metadata_chunk)
                file.truncate()

            # 新メタ情報がある場合
            if 0 < new_pointer_to_metadata_chunk:

                # メタ情報ファイルのパス
                meta_file_path = self.file_path + ".meta"

                # メタ情報ファイルを出力する
                id3 = ID3()
                self.set_tags_to_id3(id3)
                id3.save(meta_file_path, padding=(lambda x: 0))

                try:
                    # メタ情報をオーディオファイルに出力する
                    file.seek(new_pointer_to_metadata_chunk)
                    with open(meta_file_path, "rb") as meta_file:
                        metadata = meta_file.read()
                        file.write(metadata)

                finally:
                    if os.path.exists(meta_file_path):
                        os.remove(meta_file_path)

                # 以降を切り捨てる
                file.truncate

            # 合計ファイルサイズを書き換える
            total_file_size = file.tell()
            file.seek(self.total_file_size_position)
            file.write(total_file_size.to_bytes(8, "little"))


    def determine_pointer_to_metadata_chunk(self):
        """
        メタ情報チャンクの位置を決定する。
        """

        # タグ情報が何も設定されていない場合
        if not self.has_metadata():
            # 設定するメタ情報チャンクポインタは0とする
            return 0

        # 既存のタグ情報がない場合
        elif self.pointer_to_metadata_chunk == 0:
            # 設定するメタ情報チャンクポインタはファイル終端位置とする
            return os.path.getsize(self.file_path)

        # 既存のタグ情報がある場合
        else:
            # メタ情報チャンクポインタは前回と同様とする
            return self.pointer_to_metadata_chunk
