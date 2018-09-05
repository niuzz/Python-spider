# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .dbhelper import DBHelper

class WeibyPipeline(object):
    # 连接数据库
    def __init__(self):
        self.db = DBHelper()

    def process_item(self, item, spider):
        self.db.insert(item)
        return item
