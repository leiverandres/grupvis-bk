# -*- coding: utf-8 -*-
import pandas as pd
import os


class AddExtraDataPipeline(object):
    file_name = 'grupos_utp.xls'

    def open_spider(self, spider):
        '''
        Read the file where the data will be extracted from
        '''
        self.dt = pd.read_excel(
            os.path.join(os.getcwd(), 'data', self.file_name))

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        ''' 
        Handle each item, extracting extra info from excel file and
        adding it to the item dictionary
        '''
        query_code = item['code']
        row = self.dt.loc[self.dt['CODIGOGRUPO'] == query_code]
        item['faculty'] = row['FACULTAD'].values[0]
        item['dependency'] = row['DEPENDENCIA'].values[0]
        return item