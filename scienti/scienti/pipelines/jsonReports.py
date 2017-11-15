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
        newItem = {
            'products': item['products']
        }
        for cur in item['products']:
            cur['code'] = item['code']
            line = json.dumps(dict(cur)) + ",\n"
            self.file.write(line)
        return item