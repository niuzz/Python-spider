import queue
import threading
import time
import requests
import json
import pymysql
import os

exitFlag = 0

begin = time.time()

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
    'Cookie': 'Hm_lvt_29d7c655e7d1db886d67d7b9b3846aca=1535093227; Hm_lvt_b96f95878b55be2cf49fb3c099aea393=1535093227; _gscu_867320846=35093227ewx2rx38; _gscbrs_867320846=1; loginHistoryRecorded=0; TY_SESSION_ID=029480d3-77c7-48af-b0f0-0edf2d45623c; TRACK_DETECTED=1.0.1; TRACK_BROWSER_ID=fba350e3683cfa9f188aad89a0cfd5ea; username=; rememberusername=; PHPSESSID=j8c5cr4888g8ovv6dlakk8e8p6; TRACK_USER_ID=468783; TRACK_IDENTIFY_AT=2018-08-28T07%3A02%3A47.071Z; TRACK_SESSION_ID=4a8b57923fab87474507c2137f449330; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22468783%22%2C%22%24device_id%22%3A%221656aaff9d460-056137705612f9-34677908-1296000-1656aaff9d5255%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%221656aaff9d460-056137705612f9-34677908-1296000-1656aaff9d5255%22%7D; Hm_lpvt_29d7c655e7d1db886d67d7b9b3846aca=1535509121; Hm_lpvt_b96f95878b55be2cf49fb3c099aea393=1535509121; Hm_lvt_5ff3a7941ce54a1ba102742f48f181ab=1535093500,1535201562,1535509128; contactMain=1; aLastLoginTime=1535582103; _gscs_867320846=t35582099kwfbcd90|pv:2; Hm_lpvt_5ff3a7941ce54a1ba102742f48f181ab=1535582141',
    'Host': 'chuanbo.weiboyi.com',
    'Origin': 'http://chuanbo.weiboyi.com',
    'Referer': 'http://chuanbo.weiboyi.com/hworder/weixin/index',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'X-Tingyun-Id': 'y5zrBHz_BzQ;r=439778058',
}

count = 1

folder_path = './images/wechat'

qr_folder_path = './images/wechat_qrcode'


class weibyThread(threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q

    def run(self):
        print("开启线程：" + self.name)
        process_data(self.name, self.q)
        print("退出线程：" + self.name)


def save2mysql(obj):
    db = pymysql.connect(host='127.0.0.1', port=8889, user='root', passwd='root', db='article')

    cursor = db.cursor()
    global count
    sql = "INSERT INTO temp_wechat_media(name, fans, headline_price, not_headline_price, wechat_number, qrcode, category, headline_data, not_headline_data, article, media_img, media_read)" \
          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    try:

        cursor.execute(sql, (
            obj['name'], obj['fans'], obj['headline_price'], obj['not_headline_price'], obj['wechat_number'],
            obj['qrcode'], obj['category'], obj['headline_data'], obj['not_headline_data'],
            str(obj['article']), obj['media_img'], obj['read']))
        db.commit()
        time.sleep(1)
    except pymysql.InternalError as error:
        code, message = error.args
        print(">>>>>>>>>>>>>", code, message)
        db.rollback()

    print(str(count) + ':>>>>>>>>>>>>>' + str(obj))
    count += 1


def save_img(obj):
    try:
        requests.get(obj['media_img'])
    except:
        obj['media_img'] = ''
        print(obj['name'] + '没得头像')
    else:
        html = requests.get(obj['media_img'])
        arr = obj['media_img'].split('/')
        face_name = arr[len(arr) - 1]
        with open('./images/wechat/' + face_name, 'wb') as file:  # 以byte形式将图片数据写入
            file.write(html.content)
            file.flush()
        file.close()
        obj['media_img'] = '/images/wechat/' + face_name


def save_qrcode(obj):
    try:
        requests.get(obj['qrcode'])
    except:
        obj['qrcode'] = ''
        print(obj['name'] + '没得二维码')
    else:
        html = requests.get(obj['qrcode'])
        arr = obj['qrcode'].split('/')
        qr_name = arr[len(arr) - 1]
        with open('./images/wechat_qrcode/' + qr_name, 'wb') as file:  # 以byte形式将图片数据写入
            file.write(html.content)
            file.flush()
        file.close()
        obj['qrcode'] = '/images/wechat_qrcode/' + qr_name


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

    obj['article'] = lists


def get_read_num(params,
                 detail_headers,
                 obj):
    hr = requests.get(
        hotword_url,
        params=params,
        headers=detail_headers
    )
    try:
        ht = json.loads(hr.text)
    except:
        obj['hotword'] = ''
        obj['trademark'] = ''
    else:
        hr_code = ht['code']
        if hr_code == 1000:
            if ht['data']:
                obj['hotword'] = ht['data']['hotword']
                obj['trademark'] = ht['data']['trademark']
            else:
                obj['hotword'] = ''
                obj['trademark'] = ''

    br = requests.get(
        base90,
        params=params,
        headers=detail_headers
    )

    try:
        bt = json.loads(br.text)
    except:
        obj['headline_data'] = ''
        obj['not_headline_data'] = ''
    else:
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

            obj['not_headline_data'] = str(top2_avg_read) + '/' + str(top2_max_read) + ',' + str(
                top2_avg_like) + '/' + str(
                top2_max_like) + ',' + str(top2_10w)


def get_category_tag(params,
                     detail_headers,
                     obj):
    r = requests.get(
        detail_url,
        params=params,
        headers=detail_headers
    )
    try:
        t = json.loads(r.text)
    except:
        obj['category'] = ''
    else:
        tags = t['data']['type_tags']
        tag_str = ''
        for tag in tags:
            tag_str += tag + ','

        obj['category'] = tag_str


def get_item_detail(item, obj):
    arr = item['url'].split('&')
    sign = arr[2].split('=')[1]

    detail_headers = {
        'Cookie': 'Hm_lvt_29d7c655e7d1db886d67d7b9b3846aca=1535093227; Hm_lvt_b96f95878b55be2cf49fb3c099aea393=1535093227; _gscu_867320846=35093227ewx2rx38; _gscbrs_867320846=1; loginHistoryRecorded=0; TY_SESSION_ID=029480d3-77c7-48af-b0f0-0edf2d45623c; TRACK_DETECTED=1.0.1; TRACK_BROWSER_ID=fba350e3683cfa9f188aad89a0cfd5ea; Hm_lpvt_29d7c655e7d1db886d67d7b9b3846aca=1535201484; Hm_lpvt_b96f95878b55be2cf49fb3c099aea393=1535201485; Hm_lvt_5ff3a7941ce54a1ba102742f48f181ab=1535093500,1535201562; username=; rememberusername=; PHPSESSID=j8c5cr4888g8ovv6dlakk8e8p6; aLastLoginTime=1535439733; TRACK_USER_ID=468783; TRACK_IDENTIFY_AT=2018-08-28T07%3A02%3A47.071Z; TRACK_SESSION_ID=4a8b57923fab87474507c2137f449330; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22468783%22%2C%22%24device_id%22%3A%221656aaff9d460-056137705612f9-34677908-1296000-1656aaff9d5255%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%221656aaff9d460-056137705612f9-34677908-1296000-1656aaff9d5255%22%7D; Hm_lpvt_5ff3a7941ce54a1ba102742f48f181ab=1535439777; _gscs_867320846=t354397427cydi010|pv:3',
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

    save_img(obj)

    save_qrcode(obj)

    save2mysql(obj)


def get_list_item(list):
    try:
        len(list)
    except:
        print('list------------------------>' + str(list))
    else:
        for m in list:
            obj = {}
            item = m['cells']
            obj['name'] = item['original_weibo_name']
            try:
                fans_index = str(item['followers_count']).index('万')
            except:
                obj['fans'] = int(item['followers_count'])
            else:
                if fans_index > 0:
                    item_fans = str(item['followers_count']).split('万')
                    fans_str = item_fans[0].replace(',', '')
                    fans = float(fans_str) * 10000
                    fans = int(fans)
                    obj['fans'] = fans

                else:
                    obj['fans'] = int(item['followers_count'])

            try:
                item['msgitem_top_avg_read_num_28d']
            except:
                obj['read'] = 0
            else:
                obj['read'] = int(item['msgitem_top_avg_read_num_28d'])

            if item['quote']:
                try:
                    item['quote']['multi_top_original_writing']
                except:
                    try:
                        item['quote']['multi_graphic_top_price']
                    except:
                        obj['headline_price'] = item['external_reference_price']['multi_top_original_writing']['quote']
                        obj['not_headline_price'] = item['external_reference_price']['multi_second_original_writing'][
                            'quote']
                    else:

                        obj['headline_price'] = item['quote']['multi_graphic_top_price']
                        obj['not_headline_price'] = item['quote']['multi_graphic_second_price']
                else:
                    if item['quote']['multi_top_original_writing'] > item['quote']['multi_top']:
                        obj['headline_price'] = item['quote']['multi_top_original_writing']
                        obj['not_headline_price'] = item['quote']['multi_second_original_writing']
                    else:
                        try:
                            item['quote']['multi_graphic_top_price']
                        except:
                            obj['headline_price'] = item['quote']['multi_top']
                            obj['not_headline_price'] = item['quote']['multi_second']
                        else:
                            obj['headline_price'] = item['quote']['multi_graphic_top_price']
                            obj['not_headline_price'] = item['quote']['multi_graphic_second_price']

            else:

                if item['external_reference_price']:
                    obj['headline_price'] = item['external_reference_price']['multi_top_original_writing']['quote']
                    obj['not_headline_price'] = item['external_reference_price']['multi_second_original_writing']['quote']
                else:
                    obj['headline_price'] = 0.0
                    obj['not_headline_price'] = 0.0

            obj['wechat_number'] = item['weibo_id']
            if item['face_url']:

                obj['media_img'] = item['face_url']
            else:
                obj['media_img'] = item['account_avatar']
            try:
                item['screen_shot_qr_code']
            except:
                obj['qrcode'] = ''
            else:
                obj['qrcode'] = item['screen_shot_qr_code']

            get_item_detail(item, obj)


def get_list_action(page):
    payload = {
        'web_csrf_token': '5b871f976bfbb',
        'price_list': 'top, second, other, single',
        'snbt_exponent_sort': 'DESC',
        'start': page * 20,
        'limit': 20
    }
    try:
        r = requests.post(url,
                          data=payload,
                          headers=headers
                          )
    except:
        time.sleep(10)
        r = requests.post(url,
                          data=payload,
                          headers=headers
                          )
        print('!!!!!!!!!!!!!!!!!!!!!!! re connect !!!!!!!!!!!!!!!!!!!!!!!!!!')
        t = r.text
        t = json.loads(t)
        code = t['code']
        if (code == 1000):
            rows = t['data']['rows']
            get_list_item(rows)
    else:
        t = r.text
        t = json.loads(t)
        code = t['code']
        if (code == 1000):
            rows = t['data']['rows']
            get_list_item(rows)


def get_list(i):
    print('================   ' + str(i) + '   =====================')
    get_list_action(i)


def process_data(threadName, q):
    if os.path.exists(folder_path) == False:  # 判断文件夹是否已经存在
        os.makedirs(folder_path)

    if os.path.exists(qr_folder_path) == False:  # 判断文件夹是否已经存在
        os.makedirs(qr_folder_path)

    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            i = q.get()
            queueLock.release()
            get_list(i)
        else:
            queueLock.release()
        time.sleep(1)


queueLock = threading.Lock()
workQueue = queue.Queue(2000)
threads = []
threadID = 1

# 创建新线程
for tName in range(1, 51):
    thread = weibyThread(threadID, "Thread" + str(tName), workQueue)
    thread.start()
    threads.append(thread)
    threadID += 1

# 填充队列
queueLock.acquire()
for page in range(1, 1527):
    workQueue.put(page)
queueLock.release()

# 等待队列清空
while not workQueue.empty():
    pass

# 通知线程是时候退出
exitFlag = 1

# 等待所有线程完成
for t in threads:
    t.join()

during = time.time() - begin
print("退出主线程 用时：" + str(int(during) / 60) + "分钟")
