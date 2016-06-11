import io

from jp.derevijargon.tags.file_format.id3v2.ID3v2 import ID3v2
from jp.derevijargon.tags.file_format.id3v2.errors import ID3v2FormatError


class ID3v2Reader:
    """
    ID3v2パーサー

    ファイルライクオブジェクトを受け取ってタグ情報を読み込む。
    ファイルライクオブジェクトは事前にタグ情報の開始位置に読み取り位置が設定されている必要がある。
    """

    def __init__(self):
        """
        コンストラクタ。
        """
        pass


    def read(self, file):
        """
        ファイルの現在の読み取り位置からID3v2を読み込む。
        """

        # ID3v2タグ情報
        id3v2 = ID3v2()

        # ID3v2ヘッダーを読み込む
        self.read_header(file, id3v2.header)
        # バージョンを控える
        version = id3v2.header.version

        # 拡張ヘッダーがある場合
        if id3v2.header.extended_header:
            # 拡張ヘッダーを作成する
            extended_header = id3v2.create_extended_header()
            # 拡張ヘッダーを読み込む
            self.read_extended_header(extended_header, file, version)

        # 全フレームのデータを読み込む
        all_frames_data = self.read_all_frames_data(file, id3v2)
        # フレームデータを順次入力可能にする
        all_frames_data_io = io.BytesIO(all_frames_data)
        # フレームを読み込む
        self.read_frames(id3v2, all_frames_data_io)

        return id3v2


    def read_header(self, file, header):
        """
        ID3v2ヘッダーを読み込む。
        """

        # ID3v2ヘッダー
        if file.read(3) != b"ID3":
            raise ID3v2FormatError("ID3v2ヘッダーがありません。")

        # バージョン
        header.version = self.parse_version(file.read(2))

        # フラグ
        flags = file.read(1)
        unsynchronisation, extended_header, experimental_indicator, with_footer = self.parse_flags(flags, header.version)
        header.unsynchronisation = unsynchronisation
        header.extended_header = extended_header
        header.experimental_indicator = experimental_indicator
        header.with_footer = with_footer

        if unsynchronisation:
            raise ID3v2FormatError("非同期は未対応です。")

        # サイズ
        header.size = self.parse_size(file.read(4))


    def parse_version(self, version_bin):
        """
        バージョンを解釈する。
        """

        # 2バイト目が0でなければエラーとする
        if version_bin[1] != 0:
            raise ID3v2FormatError("バージョンの2バイト目が0ではありません。{}".format(version_bin[1]))

        # 1バイト目でバージョンを判断する
        first_byte = version_bin[0]
        if first_byte == 3:
            return "2.3"
        elif first_byte == 4:
            return "2.4"

        # 1バイト目が上記に該当しなければエラーとする
        raise ID3v2FormatError("バージョンの1バイト目が不正です。{}".format(first_byte))


    def parse_flags(self, flags, version):
        """
        フラグを解釈する。
        """

        # ビット演算のためintに変換する
        byte = int.from_bytes(flags, "big")

        # ID3v2.3で、上位3ビット以外がオンになっていればエラーとする
        if version == "2.3" and (byte & 0b00011111) != 0:
            raise ID3v2FormatError("フラグの値が不正です。バージョン:{} フラグ:{:b}".format(version, byte))

        # ID3v2.4で、上位4ビット以外がオンになっていればエラーとする
        elif version == "2.4" and (byte & 0b00001111) != 0:
            raise ID3v2FormatError("フラグの値が不正です。バージョン:{} フラグ:{:b}".format(version, byte))

        # 非同期
        unsynchronisation = 0b10000000 & byte
        # 拡張ヘッダー
        extended_header = 0b01000000 & byte
        # 試験段階
        experimental_indicator = 0b00100000 & byte
        # フッターあり
        with_footer = 0b00010000 & byte

        return (unsynchronisation, extended_header, experimental_indicator, with_footer)


    def parse_size(self, size_bin):
        """
        サイズを解釈する。
        """

        size = 0
        for i, b in enumerate(size_bin[::-1]):
            size += (2 ** (i * 7)) * b
        return size


    def read_extended_header(self, extended_header, file, version):
        """
        拡張ヘッダーを読み込む。
        """

        # サイズ
        extended_header.size = self.parse_size(file.read(4))

        # ID3v2.3の場合
        if version == "2.3":
            # サイズが6か10でなければエラーとする
            if extended_header.size not in (6, 10):
                raise ID3v2FormatError("拡張ヘッダーサイズが6または10ではありません。")

            # フラグ
            flags = file.read(2)
            # フラグが0でなければエラーとする
            if flags != b"\x00\x00":
                raise ID3v2FormatError("拡張フラグが0ではありません。{:b}".format(flags))

            # パディングサイズ
            extended_header.padding_size = int.from_bytes(file.read(4), "big")

            # 拡張ヘッダーサイズが10の場合は4バイトのCRCがあるので、それを読み飛ばす
            if extended_header.size == 10:
                file.seek(4, 1)

        # ID3v2.4の場合
        else:
            # サイズが6未満ならエラーとする
            if extended_header.size < 6:
                raise ID3v2FormatError("拡張ヘッダーサイズが6未満です。{}".format(extended_header.size))

            # フラグのバイト数が1でなければエラーとする
            extended_header_flag_size = file.read(1)
            if extended_header_flag_size != b"\x01":
                raise ID3v2FormatError("拡張ヘッダーフラグサイズが1ではありません。{}".format(extended_header_flag_size))

            # フラグ
            flags = int.from_bytes(file.read(1), "big")

            # タグ更新あり
            extended_header.update_tag = flags & 0b01000000
            # 添付データのサイズが0でなければエラーとする
            if extended_header.update_tag:
                size = file.read(1)
                if size != b"\x00":
                    raise ID3v2FormatError("タグ更新ありの添付データサイズが0ではありません。{}".format(size))

            # CRCデータあり
            if flags & 0b00100000:
                size = file.read(1)
                if size != b"\x05":
                    raise ID3v2FormatError("CRCの添付データサイズが5ではありません。{}".format(size))
                # CRCを読み飛ばす
                file.seek(5, 1)

            # タグ制限
            if flags & 0b00010000:
                size = file.read(1)
                if size != b"\x01":
                    raise ID3v2FormatError("タグ制限の添付データサイズが1ではありません。{}".format(size))
                # タグ制限を読み飛ばす
                file.seek(1, 1)


    def read_all_frames_data(self, file, id3v2):
        """
        全フレームのデータを読み込む。
        """

        # 全フレームのサイズ
        all_frames_size = id3v2.header.size

        # 拡張ヘッダーがある場合
        ex_header = id3v2.extended_header
        if ex_header is not None:
            # 全フレームサイズから拡張ヘッダーとパディングのサイズを除く
            all_frames_size -= ex_header.size + ex_header.padding_size

        # 全フレームを読み込む
        all_frames_data = file.read(all_frames_size)

        # 必要なデータ量が読み込めなかった場合はエラーとする
        if len(all_frames_data) < all_frames_size:
            raise ID3v2FormatError("フレーム情報がヘッダーで指定されたサイズを満たしていません。")

        return all_frames_data


    def read_frames(self, id3v2, data):
        """
        全フレームを読み込む。
        """

        # 中断されるまでループする
        while True:

            # フレームを読み込む
            if not self.read_frame(id3v2, data):
                break

            # 残りがパディングである場合は終了する
            if self.rest_all_padding(data):
                break


    def read_frame(self, id3v2, data):
        """
        フレームを読み込む。
        フレームを読み込めたかどうかを返す。
        """

        # バージョン
        version = id3v2.header.version

        # フレームID
        frame_id_bin = data.read(4)
        if len(frame_id_bin) == 0:
            return False
        if len(frame_id_bin) < 4:
            raise ID3v2FormatError("フレームIDの読み取り中にデータ終端に達しました。")
        frame_id = frame_id_bin.decode("iso-8859-1")

        # サイズ
        size_bin = data.read(4)
        if len(size_bin) < 4:
            raise ID3v2FormatError("フレームサイズの読み取り中にデータ終端に達しました。")
        size = int.from_bytes(size_bin, "big") if version == "2.3" else self.parse_size(size_bin)

        # フラグ
        flags = data.read(2)
        if len(flags) < 2:
            raise ID3v2FormatError("フレームサイズの読み取り中にデータ終端に達しました。")

        first_byte = flags[0]
        tag_alter_preservation = first_byte & 0b10000000
        file_alter_preservation = first_byte & 0b01000000
        read_only = first_byte & 0b00100000

        if first_byte & 0b00011111:
            raise ID3v2FormatError("未対応のフレームヘッダーフラグがオンです。{}".format(flags))

        unsynchronized = False
        has_data_length_indicator = False

        if version == "2.3":
            second_byte = flags[1]
            compression = second_byte & 0b10000000
            encryption = second_byte & 0b01000000
            group_identity = second_byte & 0b00100000

        else:
            group_identity = second_byte & 0b01000000
            compression = second_byte & 0b00001000
            encryption = second_byte & 0b00000100
            unsynchronized = second_byte & 0b00000010
            has_data_length_indicator = second_byte & 0b00000001


        # 圧縮フレームだったらエラーとする
        if compression:
            raise ID3v2FormatError("圧縮フレームは未対応です。")
        # 暗号化フレームだったらエラーとする
        if encryption:
            raise ID3v2FormatError("暗号化フレームは未対応です。")
        # 非同期フレームだったらエラーとする
        if unsynchronized:
            raise ID3v2FormatError("非同期フレームは未対応です。")
        # データ長インジケータがある場合はエラーとする
        if has_data_length_indicator:
            raise ID3v2FormatError("データ長インジケータは未対応です。")

        # フィールド
        field_value = data.read(size)
        if len(field_value) < size:
            raise ID3v2FormatError("フィールドの読み取り中にデータ終端に達しました。")

        # フレームIDがT空始まり、TXXXではない場合
        text = None
        if frame_id.startswith("T") and (frame_id != "TXXX"):
            # フィールドをテキスト情報として解釈する
            text = self.parse_text(field_value)

        # フレームを作成する
        frame = id3v2.create_frame()
        frame.frame_id = frame_id
        frame.size = size
        frame.tag_alter_preservation = tag_alter_preservation
        frame.file_alter_preservation = file_alter_preservation
        frame.read_only = read_only
        frame.compression = compression
        frame.group_identity = group_identity
        frame.field_value = field_value
        frame.text = text

        return True


    def parse_text(self, field_value):
        """
        フィールドをテキスト情報に変換する。
        """

        # ISO-8859-1の場合
        if field_value[0] == 0:
            if field_value[-1] != 0:
                raise ID3v2FormatError("ISO-8859-1テキスト情報が\\x00で終了していません。{}".format(field_value))
            return field_value[1:-1].decode("iso-8859-1")

        # UTF-16の場合
        if field_value[0] == 1:
            if field_value[-2:] != b"\x00\x00":
                raise ID3v2FormatError("UTF-16テキスト情報が\\x00\\x00で終了していません。{}".format(field_value))
            return field_value[1:-2].decode("utf-16")

        # v2.3なら以下はあり得ないがチェックしない

        # UTF-16BEの場合
        if field_value[0] == 2:
            if field_value[-2:] != b"\x00\x00":
                raise ID3v2FormatError("UTF-16BEテキスト情報が\\x00\\x00で終了していません。{}".format(field_value))
            return field_value[1:-2].decode("utf-16be")

        # UTF-8の場合
        if field_value[0] == 3:
            if field_value[-1] != 0:
                raise ID3v2FormatError("UTF-8テキスト情報が\\x00で終了していません。{}".format(field_value))
            return field_value[1:-1].decode("utf-8")

        raise ID3v2FormatError("テキスト情報の開始が\\x00または\\x01ではありません。{}".format(field_value))


    def rest_all_padding(self, data):
        """
        データの残りがすべてパディングであればTrueを返す。
        拡張ヘッダーがなくてもパディングが入っているファイルがあったため、
        フレームを読み込むごとに残りがパディングであるかをチェックする。
        """

        # 処理前の位置
        original_position = data.tell()

        # リターンするまでループする
        while True:
            # 1バイト読み込む
            byte = data.read(1)
            # ファイルの終端に達したらパディングだけだったとする
            if byte == b"":
                return True
            # バイト0以外があった場合
            if byte != b"\x00":
                # ファイルの読み込み位置を戻す
                data.seek(original_position)
                # パディングだけではなかったとする
                return False
