# coding: utf-8

# tagsの定数を定義するモジュール。

# タグファイル名
tag_file_name = 'tags'

# トラック情報の区切り
track_info_separator = '||'

# タグファイルのエンコーディング
tag_file_encoding = 'utf-8'

tag_file_options = dict(encoding=tag_file_encoding, newline='\n')

# 処理対象オーディオファイルの拡張子
target_exts = ('.flac', )

# タグ名
tag_album = 'ALBUM'
tag_artist = 'ARTIST'
tag_album_artist = 'ALBUMARTIST'
tag_track_total = 'TRACKTOTAL'
tag_disc_total = 'DISCTOTAL'
tag_date = 'DATE'
tag_title = 'TITLE'
tag_disc_number = 'DISCNUMBER'
tag_track_number = 'TRACKNUMBER'

# アルバムタグリスト
tag_file_album_tags = (tag_album, tag_album_artist, tag_date)
album_tags = tag_file_album_tags + (tag_disc_total, )
# ディスクタグリスト
disc_tags = (tag_disc_number, tag_track_total)
# トラックタグリスト
track_tags = (tag_title, tag_artist, tag_track_number)
# 全タグリスト
all_tags = album_tags + disc_tags + track_tags

# 削除するタグリスト
removed_tags = ('TOTALTRACKS', 'TOTALDISCS')

# 画像のMIMEから拡張子への辞書(理由は不明だが、Picture.mimeが空文字列になることが多いのでデフォルトをJPEGにする)
image_extensions = {'image/png': 'png', 'image/jpeg': 'jpg', 'image/jpg': 'jpg', 'image/gif': 'gif', '': 'jpg'}

# 画像のファイル名
image_file_name = 'Folder'

# 画像のファイル名リスト
image_files = []
for ext in image_extensions.values():
    image_files.append(image_file_name + '.' + ext)

# ファイル名から置換する文字のリスト
replace_char_list = (('*', '-'), ('\\', ''), ('|', ''), (':', ''), ('"', ''), ('<', '('), ('>', ')'), ('/', ''), ('?', ''))
