# -*- coding: utf-8 -*-


from .sql import Sql
import os
from urllib.request import urlretrieve
import requests


class WeibyPipeline(object):
    def process_item(self, item, spider):
        # self.db.insert(item)
        name = item['name']
        fans = str(item['fans'])
        read = str(item['read'])
        headline_price = str(item['headline_price'])
        not_headline_price = str(item['not_headline_price'])
        wechat_number = item['wechat_number']
        category = item['category']
        article = str(item['article'])
        headline_data = str(item['headline_data'])
        not_headline_data = item['not_headline_data']
        qrcode = item['qrcode']
        media_img = item['media_img']

        Sql.insert_dd_name(name, fans, read, headline_price,
                           not_headline_price, wechat_number,
                           category, headline_data, not_headline_data,
                           qrcode,
                           media_img,
                           article
                           )
        return item




