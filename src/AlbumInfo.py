# coding: utf-8

from const import *
from DiscInfo import DiscInfo

'''
アルバム情報
'''
class AlbumInfo:

    '''
    コンストラクタ。
    '''
    def __init__(self):
        ''' タグ情報 '''
        self.tags = {}

        ''' ディスク情報リスト '''
        self.disc_info_list = []

    '''
    ディスク情報リストを返す。
    '''
    def get_disc_info_list(self):
        return self.disc_info_list

    '''
    ディスク情報を追加する。
    '''
    def add_disc_info(self, disc_info):
        self.disc_info_list.append(disc_info)
        disc_number = str(len(self.disc_info_list))
        disc_info.tags[tag_disc_number] = disc_number
        self.tags[tag_disc_total] = disc_number

    '''
    トラック情報の件数を返す。
    '''
    def get_number_of_track_infos(self):
        return sum([len(x.get_track_info_list()) for x in self.disc_info_list])
