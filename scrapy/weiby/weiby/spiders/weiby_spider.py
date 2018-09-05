import scrapy
import json
from urllib.parse import urlencode
from urllib.parse import urljoin

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
        'Cookie': 'TY_SESSION_ID=f5cf6997-8de4-4b5f-9384-b8c892173d5a; _gscu_867320846=35093227ewx2rx38; loginHistoryRecorded=0; TRACK_DETECTED=1.0.1; TRACK_BROWSER_ID=fba350e3683cfa9f188aad89a0cfd5ea; _gscbrs_867320846=1; username=; rememberusername=; Hm_lvt_29d7c655e7d1db886d67d7b9b3846aca=1535093227,1535947850,1536054247; Hm_lvt_b96f95878b55be2cf49fb3c099aea393=1535093227,1535947850,1536054247; TY_SESSION_ID=533c08ad-b96b-4aae-8841-f62d9bd673fe; Hm_lpvt_29d7c655e7d1db886d67d7b9b3846aca=1536102233; Hm_lpvt_b96f95878b55be2cf49fb3c099aea393=1536102233; Hm_lvt_5ff3a7941ce54a1ba102742f48f181ab=1535509128,1535882186,1536047576,1536102334; PHPSESSID=9krb074p9m0vsopeh7m0jfc950; aLastLoginTime=1536102321; TRACK_USER_ID=468783; TRACK_IDENTIFY_AT=2018-09-04T23%3A05%3A59.263Z; TRACK_SESSION_ID=b9e9db51179caf466cc085fb3773d78a; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22468783%22%2C%22%24device_id%22%3A%221656aaff9d460-056137705612f9-34677908-1296000-1656aaff9d5255%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%221656aaff9d460-056137705612f9-34677908-1296000-1656aaff9d5255%22%7D; contactMain=1; _gscs_867320846=t36113473ig7n1h19|pv:4; Hm_lpvt_5ff3a7941ce54a1ba102742f48f181ab=1536115657',
        'Host': 'chuanbo.weiboyi.com',
        'Origin': 'http://chuanbo.weiboyi.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'X-Tingyun-Id': 'y5zrBHz_BzQ;r=115658164',
    }

    detail_headers = {
        'Cookie': '_gscu_867320846=35093227ewx2rx38; loginHistoryRecorded=0; TRACK_DETECTED=1.0.1; TRACK_BROWSER_ID=fba350e3683cfa9f188aad89a0cfd5ea; _gscbrs_867320846=1; username=; rememberusername=; Hm_lvt_29d7c655e7d1db886d67d7b9b3846aca=1535093227,1535947850,1536054247; Hm_lvt_b96f95878b55be2cf49fb3c099aea393=1535093227,1535947850,1536054247; TY_SESSION_ID=533c08ad-b96b-4aae-8841-f62d9bd673fe; Hm_lpvt_29d7c655e7d1db886d67d7b9b3846aca=1536102233; Hm_lpvt_b96f95878b55be2cf49fb3c099aea393=1536102233; Hm_lvt_5ff3a7941ce54a1ba102742f48f181ab=1535509128,1535882186,1536047576,1536102334; PHPSESSID=9krb074p9m0vsopeh7m0jfc950; aLastLoginTime=1536102321; TRACK_USER_ID=468783; TRACK_IDENTIFY_AT=2018-09-04T23%3A05%3A59.263Z; TRACK_SESSION_ID=b9e9db51179caf466cc085fb3773d78a; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22468783%22%2C%22%24device_id%22%3A%221656aaff9d460-056137705612f9-34677908-1296000-1656aaff9d5255%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%221656aaff9d460-056137705612f9-34677908-1296000-1656aaff9d5255%22%7D; contactMain=1; Hm_lpvt_5ff3a7941ce54a1ba102742f48f181ab=1536123584; _gscs_867320846=t36117798h5oe0819|pv:1',
        'Referer': 'http://chuanbo.weiboyi.com/reform/index',
        'User-Agen': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }

    payload = {
        'web_csrf_token': '5b8f0fb1da6a8',
        'price_list': 'top, second, other, single',
        'snbt_exponent_sort': 'DESC',
        'start': 100 * 100,
        'limit': 100
    }
    payload = urlencode(payload)

    def start_requests(self):
        url = 'http://chuanbo.weiboyi.com/hworder/weixin/filterlist/source/all'

        yield scrapy.Request(
            url=url,
            headers=self.headers,
            meta={'cookiejar': self.headers['Cookie'], 'proxy': 'http://125.125.141.101:33385'},
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
                'wechat_number': wechat_number
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
                url='http://chuanbo.weiboyi.com/single/wbyapi/getaccountbaseinfo?' + encode_payload,
                headers=self.detail_headers,
                meta={'proxy': 'http://125.125.141.101:33385',
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
            meta={'proxy': 'http://125.125.141.101:33385',
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
            meta={'proxy': 'http://125.125.141.101:33385',
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
            payload = urlencode(t_params)

            yield scrapy.Request(
                url='http://chuanbo.weiboyi.com/single/wbyapi/getarticlestop10?' + payload,
                headers=self.detail_headers,
                meta={'proxy': 'http://125.125.141.101:33385',
                      'item': item,
                      'articles': articles,
                      },
                method='GET',
                callback=self.parse_article10,
                errback=self.err_parse
            )

    def parse_article10(self, response):
        articles = response.meta['articles']
        item = response.meta['item']
        json_str = json.loads(response.text)
        articles.append(json_str['data'])
        item['article'] = articles
        yield item

    def err_parse(self, response):
        print('---------------------->>>>>>list error ')
        print(response)