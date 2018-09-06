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
    def insert_dd_name(cls, name):
        sql = 'INSERT INTO article.temp_wechat_media (`name`) VALUES (%(name)s)'
        value = {
            'name': name
        }
        cur.execute(sql, value)
        cnx.commit()
