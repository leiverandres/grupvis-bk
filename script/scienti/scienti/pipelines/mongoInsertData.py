# -*- coding: utf-8 -*-
import pymongo
import logging
from datetime import datetime


class MongoPipeline(object):
    collection_name = 'groups'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        '''
        pull in information from settings.py
        '''
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE'))

    def open_spider(self, spider):
        '''
        Open the db connection after the spider started
        '''
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        '''
        Close the DB connection
        '''
        self.client.close()

    def process_item(self, item, spider):
        ''' 
        Handle each item, inserting it in the DB or updating if
        already exist
        '''
        item['updatedAt'] = datetime.now()
        self.db[self.collection_name].update(
            {
                'code': item['code']
            }, dict(item), upsert=True)
        logging.debug("{} : Group added to DB".format(item['code']))
        return item