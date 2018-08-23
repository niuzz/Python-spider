import requests
import json
from bs4 import BeautifulSoup
import time
import re

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


def fetch_detail(rel):
    payload = {
        'action': 'viewsmedia',
        'mediaid': rel[0],
        'mediatype': 1,
    }
    r = requests.post(detail_url,
                      data=payload,
                      headers=headers)
    text = r.text
    print(text)
    text = re.match('{ .*? }', text)
    print(text)


    # soup = BeautifulSoup(text, features="html.parser")
    #
    # flag = soup.find('<!DOCTYPE')
    # print(soup)
    # time.sleep(1)


def get_detail(tr_list):
    for item in tr_list:
        bnt = item.find('div', {'class', 'bnt'})
        rela = bnt.find('a', {'class', 'viewsmedia'})
        rel = rela['rel']

        name = item.find('h3')
        name = name.find('a').text

        fetch_detail(rel)


def get_list():
    for index in range(2):
        page = index + 1
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


if __name__ == '__main__':
    main()
