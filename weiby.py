import requests
import json
import pymysql
import time

db = pymysql.connect(host='127.0.0.1', port=8889, user='root', passwd='root', db='article')

cursor = db.cursor()

url = 'http://chuanbo.weiboyi.com/hworder/weixin/filterlist/source/all'

detail_url = 'http://chuanbo.weiboyi.com/single/wbyapi/getaccountbaseinfo'

hotword_url = 'http://chuanbo.weiboyi.com/single/wbyapi/getaccountactinfo'

base90 = 'http://chuanbo.weiboyi.com/single/wbyapi/getbaseshuju'

article_top10 = 'http://chuanbo.weiboyi.com/single/wbyapi/getarticlestop10'

headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Length': '86',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': 'Hm_lvt_29d7c655e7d1db886d67d7b9b3846aca=1535093227; Hm_lvt_b96f95878b55be2cf49fb3c099aea393=1535093227; PHPSESSID=mobq2dmpgf9rssnfjef66f6gh4; _gscu_867320846=35093227ewx2rx38; _gscbrs_867320846=1; loginHistoryRecorded=0; TY_SESSION_ID=029480d3-77c7-48af-b0f0-0edf2d45623c; TRACK_USER_ID=461225; TRACK_IDENTIFY_AT=2018-08-24T06%3A51%3A40.071Z; TRACK_SESSION_ID=7df7fc3cfee9778fe5a8317a72f511fa; TRACK_DETECTED=1.0.1; TRACK_BROWSER_ID=fba350e3683cfa9f188aad89a0cfd5ea; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22461225%22%2C%22%24device_id%22%3A%221656aaff9d460-056137705612f9-34677908-1296000-1656aaff9d5255%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%221656aaff9d460-056137705612f9-34677908-1296000-1656aaff9d5255%22%7D; Hm_lpvt_29d7c655e7d1db886d67d7b9b3846aca=1535201484; Hm_lpvt_b96f95878b55be2cf49fb3c099aea393=1535201485; Hm_lvt_5ff3a7941ce54a1ba102742f48f181ab=1535093500,1535201562; contactMain=1; Hm_lpvt_5ff3a7941ce54a1ba102742f48f181ab=1535245722; username=; rememberusername=; aLastLoginTime=1535263105; _gscs_867320846=t352631017w3d6b10|pv:2',
    'Host': 'chuanbo.weiboyi.com',
    'Origin': 'http://chuanbo.weiboyi.com',
    'Referer': 'http://chuanbo.weiboyi.com/hworder/weixin/index?price_list=top%2Csecond%2Cother%2Csingle&start=0&limit=20&pageUrl=http%3A%2F%2Fchuanbo.weiboyi.com%2Fhworder%2Fweixin%2Findex%3Fprice_list%3Dtop%252Csecond%252Cother%252Csingle%26start%3D60%26limit%3D20%26pageUrl%3Dhttp%253A%252F%252Fchuanbo.weiboyi.com%252Fhworder%252Fweixin%252Findex%253Fprice_list%253Dtop%25252Csecond%25252Cother%25252Csingle%2526start%253D40%2526limit%253D20%26referrerUrl%3Dhttp%253A%252F%252Fchuanbo.weiboyi.com%252F%26app_id%3D2%26err_msg%3Derror&referrerUrl=http%3A%2F%2Fchuanbo.weiboyi.com%2F&app_id=2&err_msg=error',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'X-Tingyun-Id': 'y5zrBHz_BzQ;r=263141291',
}

count = 1


def top2mysql(obj):
    print(obj['top'])


def save2mysql(obj):
    global count
    sql = "INSERT INTO wechat_media(name, fans, headline_price, not_headline_price, wechat_number, qrcode, category, headline_data, not_headline_data)" \
          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

    art_sql = "INSERT INTO wechat_article(name, fans, headline_price, not_headline_price, wechat_number, qrcode, category, headline_data, not_headline_data)" \
          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

    article_wmid = 0

    try:
        cursor.execute(sql, (
        obj['name'],  obj['fans'], obj['headline_price'], obj['not_headline_price'], obj['wechat_number'],
        obj['qrcode'], obj['category'], obj['headline_data'], obj['not_headline_data']))
        article_wmid = cursor.lastrowid
        top2mysql(obj)
        db.commit()
    except pymysql.InternalError as error:
        code, message = error.args
        print(">>>>>>>>>>>>>", code, message)
        db.rollback()

    print(str(count) + ':' + str(obj))
    count += 1


def get_top10(params,
              detail_headers,
              obj
              ):

    order_list = [
        'msgitem_read_num',
        'msgitem_like_num',
        'msg_item_comment_count',
    ]

    lists = []
    for i in order_list:
        article_top10 = 'http://chuanbo.weiboyi.com/single/wbyapi/getarticlestop10'
        t_params = {
            'weibo_id': params['weibo_id'],
            'weibo_type': params['weibo_type'],
            'sign': params['sign'],
            'app_type': '',
            'order_by': i
        }


        tr = requests.get(
            article_top10,
            params=t_params,
            headers=detail_headers
        )

        tt = json.loads(tr.text)
        tr_code = tt['code']
        if tr_code == 1000:
            lists.append(tt['data'])

    obj['top'] = lists



def get_read_num(params,
                 detail_headers,
                 obj):
    hr = requests.get(
        hotword_url,
        params=params,
        headers=detail_headers
    )
    ht = json.loads(hr.text)
    print('hot' + str(ht['code']))
    hr_code = ht['code']
    if hr_code == 1000:
        obj['hotword'] = ht['data']['hotword']
        obj['trademark'] = ht['data']['trademark']

    time.sleep(1)

    br = requests.get(
        base90,
        params=params,
        headers=detail_headers
    )
    bt = json.loads(br.text)
    print('90days' + str(bt['code']))
    bt_code = bt['code']
    if bt_code == 1000:
        # 90头条最高阅读数
        top_max_read = bt['data']['wechat_msgitem_top_max_read_num_90d']
        # 90头条平均阅读
        top_avg_read = bt['data']['wechat_msgitem_top_de_singular_avg_read_num_90d']
        # 90头条最高点赞
        top_max_like = bt['data']['wechat_msgitem_top_max_like_num_90d']
        top_avg_like = bt['data']['wechat_msgitem_top_de_singular_avg_like_num_90d']
        top_10w = bt['data']['wechat_top_read_exceed_10w_msgitem_count_90d']

        obj['headline_data'] = str(top_avg_read) + '/' + str(top_max_read) + ',' + str(top_avg_like) + '/' + str(
            top_max_like) + ',' + str(top_10w)

        top2_max_read = bt['data']['wechat_msgitem_index2_max_read_num_90d']
        top2_avg_read = bt['data']['wechat_msgitem_index2_de_singular_avg_read_num_90d']
        top2_max_like = bt['data']['wechat_msgitem_index2_max_like_num_90d']
        top2_avg_like = bt['data']['wechat_msgitem_index2_de_singular_avg_like_num_90d']
        top2_10w = bt['data']['wechat_index2_read_exceed_10w_msgitem_count_90d']

        obj['not_headline_data'] = str(top2_avg_read) + '/' + str(top2_max_read) + ',' + str(top2_avg_like) + '/' + str(
            top2_max_like) + ',' + str(top2_10w)


def get_category_tag(params,
                     detail_headers,
                      obj ):
    r = requests.get(
        detail_url,
        params=params,
        headers=detail_headers
    )
    t = json.loads(r.text)
    print('category_tag' + str(t['code']))
    tags = t['data']['type_tags']
    tag_str = ''
    for tag in tags:
        tag_str += tag + ','

    obj['category'] = tag_str


def get_item_detail(item, obj):
    # url = detail_url + item['url']
    arr = item['url'].split('&')
    sign = arr[2].split('=')[1]

    detail_headers = {
        'Cookie': 'Hm_lvt_29d7c655e7d1db886d67d7b9b3846aca=1535093227; Hm_lvt_b96f95878b55be2cf49fb3c099aea393=1535093227; PHPSESSID=mobq2dmpgf9rssnfjef66f6gh4; _gscu_867320846=35093227ewx2rx38; _gscbrs_867320846=1; loginHistoryRecorded=0; TY_SESSION_ID=029480d3-77c7-48af-b0f0-0edf2d45623c; TRACK_USER_ID=461225; TRACK_IDENTIFY_AT=2018-08-24T06%3A51%3A40.071Z; TRACK_SESSION_ID=7df7fc3cfee9778fe5a8317a72f511fa; TRACK_DETECTED=1.0.1; TRACK_BROWSER_ID=fba350e3683cfa9f188aad89a0cfd5ea; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22461225%22%2C%22%24device_id%22%3A%221656aaff9d460-056137705612f9-34677908-1296000-1656aaff9d5255%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%221656aaff9d460-056137705612f9-34677908-1296000-1656aaff9d5255%22%7D; Hm_lpvt_29d7c655e7d1db886d67d7b9b3846aca=1535201484; Hm_lpvt_b96f95878b55be2cf49fb3c099aea393=1535201485; Hm_lvt_5ff3a7941ce54a1ba102742f48f181ab=1535093500,1535201562; contactMain=1; Hm_lpvt_5ff3a7941ce54a1ba102742f48f181ab=1535245722; username=; rememberusername=; aLastLoginTime=1535263105; _gscs_867320846=t352631017w3d6b10|pv:2',
        'Referer': 'http://chuanbo.weiboyi.com/reform/index',
        'User-Agen': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }

    params = {
        'weibo_id': item['weibo_id'],
        'weibo_type': item['weibo_type'],
        'sign': sign,
        'app_type': ''
    }

    get_category_tag(params, detail_headers, obj)

    get_read_num(params, detail_headers, obj)

    get_top10(params, detail_headers, obj)

    save2mysql(obj)


def get_list_item(list):
    for m in list:
        obj = {}
        item = m['cells']
        obj['name'] = item['original_weibo_name']
        obj['fans'] = item['followers_count'].split('万')[0]
        obj['headline_price'] = item['reference_price']['multi_top']['quote']
        obj['not_headline_price'] = item['reference_price']['multi_second']['quote']
        obj['wechat_number'] = item['weibo_id']
        obj['qrcode'] = item['screen_shot_qr_code']
        get_item_detail(item, obj)


def get_list():
    for i in range(1528):
        print('================   ' + str(i) + '   =====================')
        payload = {
            'web_csrf_token': '5b82418153742',
            'price_list': 'top, second, other, single',
            'start': 0,
            'limit': 20
        }
        r = requests.post(url,
                          data=payload,
                          headers=headers
                          )
        t = r.text
        t = json.loads(t)
        code = t['code']
        if (code == 1000):
            rows = t['data']['rows']
            get_list_item(rows)


def get_category():
    url = 'http://chuanbo.weiboyi.com/hworder/sina/allcategore'
    headers = {
        'Accept': '*/*',
        'Cookie': 'Hm_lvt_29d7c655e7d1db886d67d7b9b3846aca=1535093227; Hm_lvt_b96f95878b55be2cf49fb3c099aea393=1535093227; PHPSESSID=mobq2dmpgf9rssnfjef66f6gh4; _gscu_867320846=35093227ewx2rx38; _gscbrs_867320846=1; loginHistoryRecorded=0; TY_SESSION_ID=029480d3-77c7-48af-b0f0-0edf2d45623c; TRACK_USER_ID=461225; TRACK_IDENTIFY_AT=2018-08-24T06%3A51%3A40.071Z; TRACK_SESSION_ID=7df7fc3cfee9778fe5a8317a72f511fa; TRACK_DETECTED=1.0.1; TRACK_BROWSER_ID=fba350e3683cfa9f188aad89a0cfd5ea; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22461225%22%2C%22%24device_id%22%3A%221656aaff9d460-056137705612f9-34677908-1296000-1656aaff9d5255%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%221656aaff9d460-056137705612f9-34677908-1296000-1656aaff9d5255%22%7D; Hm_lpvt_29d7c655e7d1db886d67d7b9b3846aca=1535201484; Hm_lpvt_b96f95878b55be2cf49fb3c099aea393=1535201485; aLastLoginTime=1535201495; Hm_lvt_5ff3a7941ce54a1ba102742f48f181ab=1535093500,1535201562; contactMain=1; Hm_lpvt_5ff3a7941ce54a1ba102742f48f181ab=1535241725; _gscs_867320846=t352399283svnh813|pv:5',
        'Host': 'chuanbo.weiboyi.com',
        'Referer': 'http://chuanbo.weiboyi.com/hworder/weixin/index/source/fresh',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'X-Tingyun-Id': 'y5zrBHz_BzQ;r=241926632',

    }
    r = requests.get(url, params={'web_csrf_token': '5b8150d785cf3'}, headers=headers)
    html = json.loads(r.text)
    print('======================== 媒体列表已存储 ==============================')

    media_category_list = html['data']

    # file_object = open('wechat_category.json', 'w')
    #     # for i in html['data']:
    #     #     media = json.dumps(i)
    #     #     file_object.write(media)
    #     #     file_object.write('\n')
    #     # file_object.close()


def main():
    print('================ begin =====================')
    # get_category()
    get_list()
    print('================ closed ====================')


if __name__ == '__main__':
    main()
