# coding: utf-8

from jp.derevijargon.tags.const import *


class AlbumInfo:
    '''
    アルバム情報
    '''

    def __init__(self):
        '''
        コンストラクタ。
        '''
        ''' タグ情報 '''
        self.tags = {}

        ''' ディスク情報リスト '''
        self.disc_info_list = []

    def get_disc_info_list(self):
        '''
        ディスク情報リストを返す。
        '''
        return self.disc_info_list

    def add_disc_info(self, disc_info):
        '''
        ディスク情報を追加する。
        '''
        self.disc_info_list.append(disc_info)
        disc_number = str(len(self.disc_info_list))
        disc_info.tags[tag_disc_number] = disc_number
        self.tags[tag_disc_total] = disc_number

    def get_number_of_track_infos(self):
        '''
        トラック情報の件数を返す。
        '''
        return sum([len(x.get_track_info_list()) for x in self.disc_info_list])

