# -*- coding: utf-8 -*-


from .sql import Sql

class WeibyPipeline(object):
    # 连接数据库

    def process_item(self, item, spider):
        # self.db.insert(item)
        name = item['name']
        Sql.insert_dd_name(name)
        return item
