import scrapy
import json

class WeibySpider(scrapy.Spider):
    name = "weiby"
    allowed_domains = ["chuanbo.weiboyi.com"]

    def start_requests(self):
        url = 'http://chuanbo.weiboyi.com/hworder/weixin/filterlist/source/all';
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Length': '86',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'TY_SESSION_ID=2d4a5870-6697-41a6-b58d-ec838c408fb9; Hm_lvt_29d7c655e7d1db886d67d7b9b3846aca=1535093227; Hm_lvt_b96f95878b55be2cf49fb3c099aea393=1535093227; _gscu_867320846=35093227ewx2rx38; loginHistoryRecorded=0; TRACK_DETECTED=1.0.1; TRACK_BROWSER_ID=fba350e3683cfa9f188aad89a0cfd5ea; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22468783%22%2C%22%24device_id%22%3A%221656aaff9d460-056137705612f9-34677908-1296000-1656aaff9d5255%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%221656aaff9d460-056137705612f9-34677908-1296000-1656aaff9d5255%22%7D; PHPSESSID=gpfdeefcl4uuuspcdn6ofep753; _gscbrs_867320846=1; username=; rememberusername=; TRACK_USER_ID=468783; TRACK_IDENTIFY_AT=2018-09-02T09%3A56%3A25.851Z; TRACK_SESSION_ID=10a0f0146e95b2040663ce36352b15b3; Hm_lvt_5ff3a7941ce54a1ba102742f48f181ab=1535093500,1535201562,1535509128,1535882186; contactMain=1; aLastLoginTime=1535895561; _gscs_867320846=t35895583sticoi71|pv:3; Hm_lpvt_5ff3a7941ce54a1ba102742f48f181ab=1535895612',
            'Host': 'chuanbo.weiboyi.com',
            'Origin': 'http://chuanbo.weiboyi.com',
            'Referer': 'http://chuanbo.weiboyi.com/hworder/weixin/index?price_list=top%2Csecond%2Cother%2Csingle&snbt_exponent_sort=DESC&start=0&limit=20',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'X-Tingyun-Id': 'y5zrBHz_BzQ;r=895612513',
        }

        payload = {
            'web_csrf_token': '5b8be8093b876',
            'price_list': 'top, second, other, single',
            'snbt_exponent_sort': 'DESC',
            'start': 0 * 20,
            'limit': 20
        }

        json_body = json.dumps(payload);

        print(json_body);

        yield scrapy.FormRequest(
            url=url,
            headers=headers,
            formdata=payload,
            callback=self.parse
            );

    def parse(self, response):
        print(response);