# coding: utf-8

from const import *

'''
ディスク情報
'''
class DiscInfo:

    '''
    コンストラクタ。
    '''
    def __init__(self):
        ''' タグ情報 '''
        self.tags = {}

        ''' トラック情報リスト '''
        self.track_info_list = []

    '''
    トラック情報リストを返す。
    '''
    def get_track_info_list(self):
        return self.track_info_list

    '''
    トラック情報を追加する。
    '''
    def add_track_info(self, track_info):
        self.track_info_list.append(track_info)
        track_number = str(len(self.track_info_list))
        track_info[tag_track_number] = track_number
        self.tags[tag_track_total] = track_number
