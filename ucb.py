import requests
import json
from bs4 import BeautifulSoup
import time
import pymysql
import os
import queue
import threading
import copy as obj_copy
from xlrd import open_workbook
import xlwt
from xlutils.copy import copy

exitFlag = 0
begin = time.time()
db = pymysql.connect(host='127.0.0.1', port=8889, user='root', passwd='root', db='article')
cursor = db.cursor()

folder_path = './images/news-images/'


save_type = 'excel'


class UcbSpider:
    def __init__(self, url, img_base_url, headers, proxy):
        self.url = url
        self.img_base_url = img_base_url
        self.headers = headers
        self.proxy = proxy

    def run(self):
        print('run')
        for i in range(2):
            self.fetch_list(i)

    def fetch_list(self, page):
        current_page = page + 1
        payload = {
            'pagesize': 20,
            'pagenumber': current_page,
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
        print('下载内容开始')
        begin_time = time.time()
        r = requests.post(url, data=payload,
                          headers=headers,
                          proxies=proxy
                          )
        print('下载内容耗时', time.time() - begin_time)
        self.parse_list(r)

    def parse_list(self, r):
        s = requests.session()
        s.keep_alive = False
        text = r.text
        text = json.loads(text)
        data = text['datalist']
        soup = BeautifulSoup(data, features="html.parser")
        tr_list = soup.find_all('tr')
        for item in tr_list:
            self.parse_detail(item)

    def parse_detail(self, item):
        obj = {}
        rel = item.find('div', {'class', 'bnt'}).find('a', {'class', 'viewsmedia'})['rel']
        obj['rel'] = rel

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
        obj['type'] = mid_str
        obj['record_type'] = tds[4].text
        obj['district'] = tds[5].text
        desc = tds[6].text
        obj['desc'] = desc.strip()

        img_origin_url = tds[1].find('div', {'class', 'img'}).find('img')['src']
        fetch_img_url = self.img_base_url + img_origin_url

        self.fetch_img(fetch_img_url)

    def fetch_img(self, fetch_img_url):
        print(fetch_img_url)


if __name__ == '__main__':
    url = 'https://www.uchuanbo.com/member/ajax/news_list.php'
    detail_url = 'https://www.uchuanbo.com/member/ajax/mediaaction.php'
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7',
        'Connection': 'close',
        'Content-Length': '150',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'PHPSESSID=b29ct75dt3rc3qbi6d94mt2qf4; kefutype=0; Hm_lvt_321dd239bfd0ffe0ed3107c3da888f47=1535106618,1535944466,1536056410,1536630981; ec_im_local_status=0; CUSTOM_INVITE_CONTENT=; ec_invite_state=0; ec_invite_state_time=1536630981575; LXB_REFER=www.google.com; ec_im_tab_num=0; Hm_lpvt_321dd239bfd0ffe0ed3107c3da888f47=1536724350',
        'Host': 'www.uchuanbo.com',
        'Origin': 'https://www.uchuanbo.com',
        'Referer': 'https://www.uchuanbo.com/member/news.php?tig=red',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    proxy = {"http": "http://125.122.18.215:20953"}
    img_base_url = 'https://www.uchuanbo.com'

    UcbSpider(url, img_base_url, headers, proxy).run()


