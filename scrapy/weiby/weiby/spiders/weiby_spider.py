import scrapy
import json
from urllib.parse import urlencode
import requests
import os


class WeibySpider(scrapy.Spider):
    name = "weiby"
    allowed_domains = ["weiboyi.com"]

    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'ContentLength': '110',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': '_gscu_867320846=35093227ewx2rx38; loginHistoryRecorded=0; TRACK_DETECTED=1.0.1; TRACK_BROWSER_ID=fba350e3683cfa9f188aad89a0cfd5ea; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22468783%22%2C%22%24device_id%22%3A%221656aaff9d460-056137705612f9-34677908-1296000-1656aaff9d5255%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%221656aaff9d460-056137705612f9-34677908-1296000-1656aaff9d5255%22%7D; Hm_lvt_29d7c655e7d1db886d67d7b9b3846aca=1535093227,1535947850,1536054247,1536215671; Hm_lpvt_29d7c655e7d1db886d67d7b9b3846aca=1536215671; _gscbrs_867320846=1; Hm_lvt_b96f95878b55be2cf49fb3c099aea393=1535093227,1535947850,1536054247,1536215672; Hm_lpvt_b96f95878b55be2cf49fb3c099aea393=1536215672; PHPSESSID=ip8r13plc236f41bk7h5f977k3; web_image_site=http%3A%2F%2Fimg.weiboyi.com; TY_SESSION_ID=dc9da2bb-e5b8-41a4-84e7-daf58e35ef1e; TRACK_USER_ID=468783; TRACK_IDENTIFY_AT=2018-09-06T06%3A34%3A54.853Z; TRACK_SESSION_ID=446cc0f11aa464fa7d871ee916104a2a; Hm_lvt_5ff3a7941ce54a1ba102742f48f181ab=1535882186,1536047576,1536102334,1536215695; username=; rememberusername=; aLastLoginTime=1536265219; _gscs_867320846=t36265250folt5011|pv:3; Hm_lpvt_5ff3a7941ce54a1ba102742f48f181ab=1536265352',
        'Host': 'chuanbo.weiboyi.com',
        'Origin': 'http://chuanbo.weiboyi.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6)' +
        ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'X-Tingyun-Id': 'y5zrBHz_BzQ;r=243143174',
    }

    detail_headers = {
        'Cookie': '_gscu_867320846=35093227ewx2rx38; loginHistoryRecorded=0; TRACK_DETECTED=1.0.1; TRACK_BROWSER_ID=fba350e3683cfa9f188aad89a0cfd5ea; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22468783%22%2C%22%24device_id%22%3A%221656aaff9d460-056137705612f9-34677908-1296000-1656aaff9d5255%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%221656aaff9d460-056137705612f9-34677908-1296000-1656aaff9d5255%22%7D; Hm_lvt_29d7c655e7d1db886d67d7b9b3846aca=1535093227,1535947850,1536054247,1536215671; Hm_lpvt_29d7c655e7d1db886d67d7b9b3846aca=1536215671; _gscbrs_867320846=1; Hm_lvt_b96f95878b55be2cf49fb3c099aea393=1535093227,1535947850,1536054247,1536215672; Hm_lpvt_b96f95878b55be2cf49fb3c099aea393=1536215672; PHPSESSID=ip8r13plc236f41bk7h5f977k3; web_image_site=http%3A%2F%2Fimg.weiboyi.com; TY_SESSION_ID=dc9da2bb-e5b8-41a4-84e7-daf58e35ef1e; TRACK_USER_ID=468783; TRACK_IDENTIFY_AT=2018-09-06T06%3A34%3A54.853Z; TRACK_SESSION_ID=446cc0f11aa464fa7d871ee916104a2a; Hm_lvt_5ff3a7941ce54a1ba102742f48f181ab=1535882186,1536047576,1536102334,1536215695; username=; rememberusername=; aLastLoginTime=1536265219; _gscs_867320846=t36265250folt5011|pv:2; Hm_lpvt_5ff3a7941ce54a1ba102742f48f181ab=1536265268',
        'Referer': 'http://chuanbo.weiboyi.com/reform/index',
        'User-Agen': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }

    payload = {
        'web_csrf_token': '5b918c03a9a79',
        'price_list': 'top, second, other, single',
        'snbt_exponent_sort': 'DESC',
        'start': 1 * 10,
        'limit': 20
    }
    payload = urlencode(payload)

    proxy = 'http://122.230.43.139:33055'

    folder_path = './images/wechat'

    qr_folder_path = './images/wechat_qrcode'

    def __init__(self):
        if os.path.exists(self.folder_path) == False:  # 判断文件夹是否已经存在
            os.makedirs(self.folder_path)

        if os.path.exists(self.qr_folder_path) == False:  # 判断文件夹是否已经存在
            os.makedirs(self.qr_folder_path)

    def start_requests(self):
        url = 'http://chuanbo.weiboyi.com/hworder/weixin/filterlist/source/all'
        url1 = 'http://chuanbo.weiboyi.com/hworder/weixin/index?price_list=top%2Csecond%2Cother%2Csingle&snbt_exponent_sort=DESC&start=0&limit=20'
        yield scrapy.Request(
            url=url,
            headers=self.headers,
            meta={
                'cookiejar': self.headers['Cookie'],
                # 'proxy': self.proxy
                  },
            method='POST',
            body=self.payload,
            callback=self.parse,
            errback=self.err_parse,
        )


    def parse(self, response):
        result = json.loads(response.text)
        rows = result['data']['rows']
        count = 0
        for item in rows:
            row = item['cells']

            name = row['original_weibo_name']

            fans_str = row['followers_count']
            fans_str_index = str(fans_str).find('万')
            if fans_str_index > -1:
                fans_str = str(fans_str).replace('万', '')
                fans_str = str(fans_str).replace(',', '')
                fans_str = int(float(fans_str) * 10000)
            else:
                fans_str = int(str(fans_str))

            read = row['msgitem_top_avg_read_num_28d']

            if 'screen_shot_qr_code' in row:
                qrcode = row['screen_shot_qr_code']

            else:
                qrcode = ''

            if 'face_url' in row:
               media_img = row['face_url']
            else:
                media_img = ''

            local_qrcode = self.save_qrcode(qrcode)
            local_media_img = self.save_img(media_img)

            qrcode = local_qrcode
            media_img = local_media_img
            if ('multi_top' in row['quote']):
                headline_price = row['quote']['multi_top']
            else:
                headline_price = row['quote']['multi_graphic_top_price']

            if ('multi_second' in row['quote']):
                not_headline_price = row['quote']['multi_second']
            else:
                not_headline_price = row['quote']['multi_graphic_second_price']

            wechat_number = row['weibo_id']

            item = {
                'count': count,
                'name': name,
                'fans': fans_str,
                'read': read,
                'headline_price': headline_price,
                'not_headline_price': not_headline_price,
                'wechat_number': wechat_number,
                'qrcode': qrcode,
                'media_img': media_img
            }

            tmp_arr = row['url'].split('&')
            sign = tmp_arr[2].split('=')[1]
            payload = {
                'weibo_id': row['weibo_id'],
                'weibo_type': row['weibo_type'],
                'sign': sign,
                'app_type': ''
            }
            encode_payload = urlencode(payload)



            yield scrapy.Request(
                url='http://chuanbo.weiboyi.com/single/wbyapi/' +
                'getaccountbaseinfo?' + encode_payload,
                headers=self.detail_headers,
                meta={
                    # 'proxy': self.proxy,
                    'item': item,
                    'payload': encode_payload,
                    'decode_payload': payload
                    },
                method='GET',
                callback=self.parse_category,
            )
            count += 1

    def parse_category(self, response):
        item = response.meta['item']
        json_str = json.loads(response.text)
        tags = json_str['data']['type_tags']
        tag_str = ''
        for tag in tags:
            if tag != tags[-1]:
                tag_str += tag + ','
            else:
                tag_str += tag
        item['category'] = tag_str

        payload = response.meta['payload']
        yield scrapy.Request(
            url='http://chuanbo.weiboyi.com/single/wbyapi/getaccountactinfo?' + payload,
            headers=self.detail_headers,
            meta={
                  # 'proxy': self.proxy,
                  'item': item,
                  'payload': payload,
                  'decode_payload': response.meta['decode_payload']
                  },
            method='GET',
            callback=self.parse_hotword,
        )

    def parse_hotword(self, response):
        item = response.meta['item']
        json_str = json.loads(response.text)
        hotword = json_str['data']['hotword']
        trademark = json_str['data']['trademark']
        if hotword:
            item['hotword'] = hotword
            item['trademark'] = trademark
        else:
            item['hotword'] = ''
            item['trademark'] = ''
        payload = response.meta['payload']

        yield scrapy.Request(
            url='http://chuanbo.weiboyi.com/single/wbyapi/getbaseshuju?' + payload,
            headers=self.detail_headers,
            meta={
                # 'proxy': self.proxy,
                  'item': item,
                  'payload': payload,
                  'decode_payload': response.meta['decode_payload']
                  },
            method='GET',
            callback=self.parse_read_data,
        )

    def parse_read_data(self, response):
        item = response.meta['item']
        bt = json.loads(response.text)
        # 90头条最高阅读数
        top_max_read = bt['data']['wechat_msgitem_top_max_read_num_90d']
        # 90头条平均阅读
        top_avg_read = bt['data']['wechat_msgitem_top_de_singular_avg_read_num_90d']
        # 90头条最高点赞
        top_max_like = bt['data']['wechat_msgitem_top_max_like_num_90d']
        top_avg_like = bt['data']['wechat_msgitem_top_de_singular_avg_like_num_90d']
        top_10w = bt['data']['wechat_top_read_exceed_10w_msgitem_count_90d']

        item['headline_data'] = str(top_avg_read) + '/' + str(top_max_read) + ',' + str(top_avg_like) + '/' + str(
            top_max_like) + ',' + str(top_10w)

        top2_max_read = bt['data']['wechat_msgitem_index2_max_read_num_90d']
        top2_avg_read = bt['data']['wechat_msgitem_index2_de_singular_avg_read_num_90d']
        top2_max_like = bt['data']['wechat_msgitem_index2_max_like_num_90d']
        top2_avg_like = bt['data']['wechat_msgitem_index2_de_singular_avg_like_num_90d']
        top2_10w = bt['data']['wechat_index2_read_exceed_10w_msgitem_count_90d']

        item['not_headline_data'] = str(top2_avg_read) + '/' + str(top2_max_read) + ',' + str(
            top2_avg_like) + '/' + str(top2_max_like) + ',' + str(top2_10w)

        order_list = [
            'msgitem_read_num',
            'msgitem_like_num',
            'msg_item_comment_count',
        ]

        articles = []

        for i in order_list:
            t_params = response.meta['decode_payload']
            t_params['order_by'] = i
            article_top10 = 'http://chuanbo.weiboyi.com/single/wbyapi/getarticlestop10'
            tr = requests.get(
                article_top10,
                params=t_params,
                headers=self.detail_headers,
                # proxies={'http': self.proxy},
            )

            tt = json.loads(tr.text)
            tr_code = tt['code']
            if tr_code == 1000:
                articles.append(tt['data'])

        item['article'] = articles
        yield item

    def save_qrcode(self, qrcode):
        if qrcode:
            html = requests.get(qrcode,
                                headers=self.detail_headers,
                                # proxies={'http': self.proxy}
                                )
            arr = qrcode.split('/')
            qr_name = arr[len(arr) - 1]
            with open('./images/wechat_qrcode/' + qr_name, 'wb') as file:  # 以byte形式将图片数据写入
                file.write(html.content)
                file.flush()
            file.close()
            return '/images/wechat_qrcode/' + qr_name
        else:
            return ''

    def save_img(self, media_img):
        if media_img:
            html = requests.get(media_img)
            arr = media_img.split('/')
            media_img_name = arr[len(arr) - 1]
            with open('./images/wechat/' + media_img_name, 'wb') as file:  # 以byte形式将图片数据写入
                file.write(html.content)
                file.flush()
            file.close()
            return '/images/wechat/' + media_img_name
        else:
            return ''


    def err_parse(self, response):
        print('---------------------->>>>>>list error ')
        print(response)
