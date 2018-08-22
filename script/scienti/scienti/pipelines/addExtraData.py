# -*- coding: utf-8 -*-
import pandas as pd
import os


class AddExtraDataPipeline(object):
    ## Info provided by UTP
    utp_data_file_name = "grupos_utp.xls"
    ## Info extracted in past versions of this script
    results_737_file_name = "clasificación_2015.csv"
    ## Info published by Colciencias
    results_781_file_name = "resultados_finales_781_6-12-2017.xlsx"

    def open_spider(self, spider):
        '''
        Read the file where the data will be extracted from
        '''
        utp_data_path = os.path.join("data", self.utp_data_file_name)
        results_737_path = os.path.join("data", self.results_737_file_name)
        results_781_path = os.path.join("data", self.results_781_file_name)
        self.dt_utp = pd.read_excel(utp_data_path)
        self.dt_737 = pd.read_csv(results_737_path)
        self.dt_781 = pd.read_excel(results_781_path, sheet_name="UTP")

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        ''' 
        Handle each item, extracting extra info from excel or csv files and
        adding it to the item dictionary
        '''
        querycode = item["code"]

        ## Extracting data from utp data
        try:
            row_utp = self.dt_utp.loc[self.dt_utp["CODIGOGRUPO"] == querycode]
            item["faculty"] = row_utp["FACULTAD"].values[0]
            item["dependency"] = row_utp["DEPENDENCIA"].values[0]
        except IndexError:
            item["faculty"] = ""
            item["dependency"] = ""
        # Extracting data from classification 737
        row_737 = self.dt_737[self.dt_737["code"] == querycode]
        if not row_737.empty:
            classification2015 = str(row_737["clasification"].values[0])
            if classification2015 != "nan":
                item["classification2015"] = classification2015.strip()
            else:
                item["classification2015"] = ""
        else:
            item["classification2015"] = ""
        # Extracting data from classification 781
        row_781 = self.dt_781[self.dt_781["CÓDIGO DE GRUPO"] == querycode]
        if not row_781.empty:
            try:
                item["classification2017"] = row_781[
                    "CLASIFICACIÓN DEL GRUPO"].values[0]
            except IndexError:
                print("This group failed", querycode, ". Empty condition:",
                      row_781.empty)
        else:
            item["classification2017"] = ""
            print("Hell yes!")
        return item