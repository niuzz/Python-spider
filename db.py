import pymysql

db = pymysql.connect(host='127.0.0.1', port=8889, user='root', passwd='root', db='article')

cursor = db.cursor()

sql = "INSERT INTO test(name) VALUES ('%s')" % \
      ('dddd')

try:
    cursor.execute(sql)
    db.commit()
except:
    db.rollback()

cursor.close()
db.close()