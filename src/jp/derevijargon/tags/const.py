# coding: utf-8

# tagsの定数を定義するモジュール。

# タグファイルを開く際のオプション
tag_file_open_options = dict(encoding="utf-8", newline="\n")

# タグファイル名
tag_file_name = "tags"

# アーティストの区切り
artist_separator = "//"

# タグファイルのエンコーディング
tag_file_encoding = "utf-8"

# 処理対象オーディオファイルの拡張子
target_exts = (".flac", )

# 削除するタグリスト
removed_tags = ("TOTALTRACKS", "TOTALDISCS")
