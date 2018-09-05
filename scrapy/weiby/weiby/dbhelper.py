# -*- coding: utf-8 -*-

import pymysql
from twisted.enterprise import adbapi
from scrapy.utils.project import get_project_settings  #导入seetings配置
import time


class DBHelper():

    def __init__(self):
        settings = get_project_settings()  #获取settings配置，设置需要的信息

        dbparams = dict(
            host=settings['MYSQL_HOST'],  #读取settings中的配置
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWORD'],
            port=settings['MYSQL_PORT'],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=False,
        )
        dbpool = adbapi.ConnectionPool('pymysql', **dbparams)

        self.dbpool = dbpool

    def connect(self):
        return self.dbpool

    #写入数据库
    def insert(self, item):
        sql = "insert into temp_wechat_media(name, fans) values(%s, %s)"
        #调用插入的方法
        query = self.dbpool.runInteraction(self._conditional_insert, sql, item)
        #调用异常处理方法
        query.addErrback(self._handle_error)

        return item

    def _conditional_insert(self, tx, sql, item):
        print('=================>>>>>>>>>>>>>>>>>>>')
        print(sql)
        params = (item["name"], item['fans'])
        tx.execute(sql, params)

    #错误处理方法

    def _handle_error(self, failue):
        print('--------------database operation exception!!-----------------')
        print(failue)