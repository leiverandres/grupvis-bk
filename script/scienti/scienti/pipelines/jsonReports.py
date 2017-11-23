# -*- coding: utf-8 -*-
import json


class JSONResporterPipeline(object):
    def open_spider(self, spider):
        '''
        Open file to write
        '''
        self.file = open('resport.jl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        item_to_save = item.copy()

        for cur in item_to_save['products']:
            cur['code'] = item_to_save['code']
            line = json.dumps(dict(cur)) + ",\n"
            self.file.write(line)
        return item