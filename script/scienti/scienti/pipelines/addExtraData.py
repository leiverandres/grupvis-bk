# -*- coding: utf-8 -*-
import pandas as pd
import os


class AddExtraDataPipeline(object):
    ## info provided by UTP
    utp_file_name = 'grupos_utp.xls'
    ## info published by Colciencias
    preliminary_result_file_name = "resultados-preliminares-grupos-conv_781.xlsx"

    def open_spider(self, spider):
        '''
        Read the file where the data will be extracted from
        '''
        utp_path = os.path.join('data', self.utp_file_name)
        colci_path = os.path.join('data', self.preliminary_result_file_name)
        self.dt_utp = pd.read_excel(utp_path)
        self.dt_colci = pd.read_excel(colci_path)

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        ''' 
        Handle each item, extracting extra info from excel file and
        adding it to the item dictionary
        '''
        querycode = item['code']

        ## Extracting data from utp data
        row_utp = self.dt_utp.loc[self.dt_utp['CODIGOGRUPO'] == querycode]
        item['faculty'] = row_utp['FACULTAD'].values[0]
        item['dependency'] = row_utp['DEPENDENCIA'].values[0]

        # Extracting data from utp
        row_c = self.dt_colci[self.dt_colci['CÓDIGO DE GRUPO'] == querycode]
        if not row_c.empty:
            item['classification2017'] = row_c[
                'CLASIFICACIÓN DEL GRUPO'].values[0]
        else:
            item['classification2017'] = ''
        return item