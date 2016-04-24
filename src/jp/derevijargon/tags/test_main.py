# coding: utf-8

import os

from nose import *

import main
from jp.derevijargon.tags.export_service import execute as export_service
from jp.derevijargon.tags.import_service import execute as import_service
from jp.derevijargon.tags.rename_service import execute as rename_service
from jp.derevijargon.tags.const import *


"""
タグファイルを作成する。
"""
def create_tag_file():
    open(tag_file_name, "w").close()

"""
タグファイルを削除する。
"""
def remove_tag_file():
    if os.path.exists(tag_file_name):
        os.remove(tag_file_name)

"""
明示的にエクスポート処理を選択する。
"""
def test_select_service_select_export_explicit():
    service = main.select_service(["e"])
    assert service is export_service

"""
明示的にインポート処理を選択する。
"""
def test_select_service_select_import_explicit():
    service = main.select_service(["i"])
    assert service is import_service

"""
明示的にリネーム処理を選択する。
"""
def test_select_service_select_rename_explicit():
    service = main.select_service(["r"])
    assert service is rename_service

"""
暗黙的にエクスポート処理を選択する。
"""
@with_setup(setup=remove_tag_file)
def test_select_service_select_export_implicit():
    service = main.select_service([])
    assert service is export_service

"""
暗黙的にインポート処理を選択する。
"""
@with_setup(create_tag_file, remove_tag_file)
def test_select_service_select_import_implicit():
    service = main.select_service([])
    assert service is import_service
