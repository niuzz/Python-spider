import mysql.connector

MYSQL_HOSTS = '127.0.0.1'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'root'
MYSQL_PORT = '8889'
MYSQL_DB = 'article'

cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD, host=MYSQL_HOSTS, port=MYSQL_PORT, database=MYSQL_DB)
cur = cnx.cursor(buffered=True)

class Sql:

    @classmethod
    def insert_dd_name(cls, name, fans, read, headline_price, not_headline_price, wechat_number, category,
                       headline_data, not_headline_data, qrcode, media_img, article):
        sql = 'INSERT INTO article.temp_wechat_media (`name`,`fans_num`, `read_num`, `headline_price`, `not_headline_price`,' \
              '`wechat_number`, `category`, `article`, `headline_data`, `not_headline_data`, `qrcode`, `media_img`) ' \
              'VALUES (%(name)s, %(fans_num)s, %(read_num)s, %(headline_price)s, %(not_headline_price)s, %(wechat_number)s,' \
              '%(category)s, %(article)s, %(headline_data)s, %(not_headline_data)s, %(qrcode)s, %(media_img)s)'
        value = {
            'name': name,
            'fans_num': fans,
            'read_num': read,
            'headline_price': headline_price,
            'not_headline_price': not_headline_price,
            'wechat_number': wechat_number,
            'category': category,
            'article': article,
            'headline_data': headline_data,
            'not_headline_data': not_headline_data,
            'qrcode': qrcode,
            'media_img': media_img
        }
        cur.execute(sql, value)
        cnx.commit()
