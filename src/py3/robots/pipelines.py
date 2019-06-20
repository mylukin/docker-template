# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from robots.items import *


class RobotsPipeline(object):
    def process_item(self, item, spider):
        return item


class Save2MongoPipeline(object):

    tables = ['words', 'xings']

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB', 'qiming')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

        for table in self.tables:
            if table == 'xings':
                self.db[table].create_index('name', unique=True)
            if table == 'words':
                self.db[table].create_index('name', unique=True)

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        collection_name = 'items'

        if isinstance(item, ZdicWordItem):
            collection_name = 'words'

        if isinstance(item, XingItem):
            collection_name = 'xings'

        try:
            self.db[collection_name].insert_one(dict(item))
        except pymongo.errors.DuplicateKeyError:
            pass
        return item
