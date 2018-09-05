# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeibyItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    media_img = scrapy.Field()
    fans = scrapy.Field()
    read = scrapy.Field()
    headline_price = scrapy.Field()
    not_headline_price = scrapy.Field()
    wechat_number = scrapy.Field()
    qrcode = scrapy.Field()
    category = scrapy.Field()
    headline_data = scrapy.Field()
    not_headline_data = scrapy.Field()
    article = scrapy.Field()
    pass
