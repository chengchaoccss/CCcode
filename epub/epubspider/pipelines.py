# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import os
import json

class EpubPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoPipeline(object):
    def __init__(self,mongo_uri,mongo_db):
        self.mongo_uri=mongo_uri
        self.mongo_db=mongo_db

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self,spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db=self.client[self.mongo_db]

    def process_item(self,item,spider):
        name=item.__class__.__name__
        self.db[name].insert(dict(item))
        return item

    def close_spider(self,spider):
        self.client.close()

class JsonPipeline(object):
    def process_item(self, item, spider):
        base_dir = os.getcwd()
        filename = base_dir + '/news.json'
        # 打开json文件，向里面以dumps的方式吸入数据
        # 注意需要有一个参数ensure_ascii=False ，不然数据会直接为utf编码的方式存入比如
        # :“/xe15”
        with open(filename, 'a') as f:
            line = json.dumps(dict(item), ensure_ascii=False) + '\n'
            f.write(line)
        return item
