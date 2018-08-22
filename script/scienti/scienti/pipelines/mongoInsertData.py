# -*- coding: utf-8 -*-
import pymongo
from scrapy.conf import settings
from datetime import datetime


class MongoPipeline(object):
    def open_spider(self, spider):
        '''
        Open the db connection after the spider started
        '''
        self.client_connection = pymongo.MongoClient(settings['MONGO_URI'])
        self.db = self.client_connection[settings['MONGO_DATABASE']]
        self.collection = self.db[settings['MONGO_COLLECTION']]

    def close_spider(self, spider):
        '''
        Close the DB connection
        '''
        self.client_connection.close()

    def process_item(self, item, spider):
        ''' 
        Handle each item, inserting it in the DB or updating if
        already exist
        '''
        item['updatedAt'] = datetime.now()
        self.collection.update({'code': item['code']}, dict(item), upsert=True)
        return item