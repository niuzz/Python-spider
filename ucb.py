import requests
import json
from bs4 import BeautifulSoup
import time
import pymysql

db = pymysql.connect(host='127.0.0.1', port=8889, user='root', passwd='root', db='article')

cursor = db.cursor()

obj = {}

url = 'https://www.uchuanbo.com/member/ajax/news_list.php'
detail_url = 'https://www.uchuanbo.com/member/ajax/mediaaction.php'
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7',
    'Connection': 'keep-alive',
    'Content-Length': '150',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': 'PHPSESSID=mcu4jn5gdirofjnakfrfn4tj62; OUTFOX_SEARCH_USER_ID_NCOO=479025887.6639701; Hm_lvt_321dd239bfd0ffe0ed3107c3da888f47=1534945762; ec_im_local_status=0; CUSTOM_INVITE_CONTENT=; ec_invite_state=0; LXB_REFER=www.google.com; ec_invite_state_time=1534945783551; ec_im_tab_num=0; kefutype=0; Hm_lpvt_321dd239bfd0ffe0ed3107c3da888f47=1534945797',
    'DNT': '1',
    'Host': 'www.uchuanbo.com',
    'Origin': 'https://www.uchuanbo.com',
    'Referer': 'https://www.uchuanbo.com/member/news.php',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}


def save2Mysql():
    # sql = "INSERT INTO temp_news_media(name, mcid, desc, type, direct_price, case, trade_category, district, record_type, send_media, interlinkage_type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    #     (obj['name'], obj['mcid'], obj['desc'], obj['type'], obj['direct_price'], obj['case'], obj['trade_category'], obj['district'], obj['record_type'], obj['send_media'], obj['interlinkage_type'])

    sql = "INSERT INTO temp_news_media(name, mcid, direct_price, type, trade_category, district, record_type, send_media, interlinkage_type, case_link, media_desc)" \
          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"


    try:
        cursor.execute(sql, (obj['name'], obj['mcid'], obj['direct_price'], obj['type'], obj['trade_category'], obj['district'], obj['record_type'], obj['send_media'], obj['interlinkage_type'], obj['case'], obj['desc']))
        db.commit()
    except pymysql.InternalError as error:
        code, message = error.args
        print(">>>>>>>>>>>>>", code, message)
        db.rollback()
    print(obj)


def fetch_detail(rel):
    payload = {
        'action': 'viewsmedia',
        'mediaid': rel[0],
        'mediatype': 1,
    }
    r = requests.post(detail_url,
                      data=payload,
                      headers=headers)
    r.encoding = 'utf8'
    text = r.text
    try:
        text = json.loads(text)
    except:
        obj['interlinkage_type'] = ''
        obj['type'] = ''
        obj['send_media'] = ''
        save2Mysql()
    else:
        text = text['contacthtml']

        soup = BeautifulSoup(text, features="html.parser")
        table = soup.find('table')
        tds = table.find_all('td')
        obj['interlinkage_type'] = tds[7].text
        obj['type'] = tds[2].text
        obj['trade_category'] = tds[2].text
        str = tds[8].find('em').text + ',' + tds[9].find('em').text
        obj['send_media'] = str

        save2Mysql()

    time.sleep(1)


def get_detail(tr_list):
    for item in tr_list:
        bnt = item.find('div', {'class', 'bnt'})
        rela = bnt.find('a', {'class', 'viewsmedia'})
        rel = rela['rel']

        name = item.find('h3')
        name = name.find('a').text
        obj['name'] = name

        case = item.find('div', {'class', 'text'})
        case = case.find('p')
        case = case.find('a')
        case = case['href']
        obj['case'] = case

        price = item.find('td', {'class', 'price'}).text
        price = price.split('￥')[1]
        try:
            price = float(price)
        except ValueError:
            price = 0.0
        obj['direct_price'] = price

        tds = item.find_all('td')

        mid_str = tds[3].text
        obj['type'] = tds[3].text
        mcid = 0
        if mid_str == '综合门户':
            mcid = 0
        elif mid_str == '中央媒体':
            mcid = 1
        elif mid_str == '地方门户':
            mcid = 2
        elif mid_str == '垂直媒体':
            mcid = 3
        elif mid_str == '中小媒体':
            mcid = 4
        elif mid_str == '自媒体':
            mcid = 5

        obj['mcid'] = mcid
        obj['record_type'] = tds[4].text
        obj['district'] = tds[5].text
        desc = tds[6].text
        obj['desc'] = desc.strip()

        fetch_detail(rel)


def get_list():
    for index in range(410):
        page = index + 1
        print('========================' + str(page) + '==============================')
        payload = {
            'pagesize': 20,
            'pagenumber': page,
            'keywords': '',
            'category': '0',
            'portal': 0,
            'area': 0,
            'prange': '0,100000000',
            'record': 0,
            'cansend': 0,
            'linktype': 0,
            'media_u_type': 0,
            'orderby': 'listorder DESC'
        }

        r = requests.post(url, data=payload,
                          headers=headers
                          )

        text = r.text
        text = json.loads(text)
        data = text['datalist']

        soup = BeautifulSoup(data, features="html.parser")
        tr_list = soup.find_all('tr')

        time.sleep(1)

        get_detail(tr_list)




def main():
    get_list()
    db.close()
    print('-------close db-------')


if __name__ == '__main__':
    main()
