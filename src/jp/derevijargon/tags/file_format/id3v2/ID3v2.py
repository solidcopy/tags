from jp.derevijargon.tags.file_format.id3v2.errors import ID3v2FormatError
from jp.derevijargon.tags.meta.Image import Image


class ID3v2:
    """
    ID3v2タグ情報
    """

    def __init__(self):
        """
        コンストラクタ。
        """

        # ヘッダー
        self._header = ID3v2Header()
        # 拡張ヘッダー
        self._extended_header = None
        # フレームリスト
        self._frame_list = []

    header = property((lambda self: self._header), doc="ID3v2ヘッダー")

    extended_header = property((lambda self: self._extended_header), doc="拡張ヘッダー")

    frame_list = property((lambda self: self._frame_list[:]), doc="フレームリスト")


    def create_extended_header(self):
        """
        拡張ヘッダーを作成する。
        """

        self._extended_header = ID3v2ExtendedHeader()
        return self._extended_header


    def create_frame(self):
        """
        フレームを作成する
        """

        frame = ID3v2Frame()
        self._frame_list.append(frame)
        return frame


    def get_frame(self, frame_id):
        """
        指定されたフレームIDに該当するフレームを返す。
        複数該当がある場合は最初に見つかったものを返す。
        """

        # フレームをループする
        for a_frame in self._frame_list:
            # フレームIDが一致する場合
            if a_frame.frame_id == frame_id:
                # このフレームを返す
                return a_frame

        return None


    def __getitem__(self, frame_id):
        """
        指定されたフレームのフィールドを返す。
        フレームがテキストフレームならテキスト情報を返す。
        """

        # フレームをループする
        for a_frame in self._frame_list:
            # フレームIDが一致する場合
            if a_frame.frame_id == frame_id:
                # テキスト情報か、なければフィールドをリストに追加する
                return a_frame.text or a_frame.field_value

        return None


    def get_all(self, frame_id):
        """
        指定されたフレームの全フィールドを返す。
        フレームがテキストフレームならテキスト情報を返す。
        """

        value_list = []

        # フレームをループする
        for a_frame in self._frame_list:
            # フレームIDが一致する場合
            if a_frame.frame_id == frame_id:
                # テキスト情報か、なければフィールドをリストに追加する
                value = a_frame.text or a_frame.field_value
                value_list.append(value)

        return value_list


class ID3v2Header:
    """
    ID3v2ヘッダー
    """

    def __init__(self):
        """
        コンストラクタ。
        """

        self.version = None
        """バージョン"""
        self.unsynchronisation = False
        """非同期"""
        self.extended_header = False
        """拡張ヘッダー"""
        self.experimental_indicator = False
        """試験段階"""
        self.with_footer = False
        """フッターあり"""
        self.size = None
        """サイズ"""


class ID3v2ExtendedHeader:
    """
    ID3v2拡張ヘッダー
    """

    def __init__(self):
        """
        コンストラクタ。
        """

        self.extended_header_size = None
        """拡張ヘッダーサイズ"""
        self.padding_size = None
        """パディングサイズ"""
        self.update_tag = False
        """タグを上書きするか"""



class ID3v2Frame:
    """
    ID3v2フレーム
    """

    def __init__(self):
        """
        コンストラクタ。
        """

        self.frame_id = None
        """フレームID"""
        self.size = None
        """サイズ"""

        self.tag_alter_preservation = False
        """タグが編集されたとき、このタグを知らない場合は切り捨てるか"""
        self.file_alter_preservation = False
        """タグ以外が編集されたとき、このタグを知らない場合は切り捨てるか"""
        self.read_only = False
        """読み取り専用であるか"""
        self.compression = False
        """タグが圧縮されているか"""
        self.encryption = False
        """タグが暗号化されているか"""
        self.group_identity = None
        """グループ識別"""
        self.field_value = None
        """フィールド"""
        self.text = None
        """テキスト情報"""


    def as_image(self):
        """
        このフレームをImageに変換する。
        """

        # フィールド読み取りインデックス
        i = 0
        # アクセスしやすくする
        v = self.field_value

        # テキストエンコーディングを読み込む
        text_encoding = v[i]
        if text_encoding not in (0, 1):
            raise ID3v2FormatError("画像のテキストエンコーディングが不正です。{}".format(text_encoding))
        i += 1

        # MIMEを読み込む
        mime_end = v.find(b"\x00", i)
        if mime_end == -1:
            raise ID3v2FormatError("MIMEの終端がありません。")
        mime = v[i:mime_end]
        mime = mime.decode("iso-8859-1")
        i = mime_end + 1

        # 画像タイプは読み飛ばす
        i += 1

        # 説明を読み飛ばす
        end = b"\x00" if text_encoding == 0 else b"\x00\x00"
        desc_end = v.find(end, i)
        if desc_end == -1:
            raise ID3v2FormatError("画像説明の終端がありません。")
        i = desc_end + len(end)

        # 画像データを読み込む
        data = v[i:]

        return Image.create_from_data(mime, data)
