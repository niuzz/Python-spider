import requests

article_top10 = 'http://chuanbo.weiboyi.com/single/wbyapi/getarticlestop10'

params = {
        'weibo_id': 'yetingfm',
        'weibo_type': '9',
        'sign': '785b5c400d',
        'app_type': '',
        'order_by': 'msgitem_read_num'
    }

detail_headers = {
        'Cookie': 'Hm_lvt_29d7c655e7d1db886d67d7b9b3846aca=1535093227; Hm_lvt_b96f95878b55be2cf49fb3c099aea393=1535093227; PHPSESSID=mobq2dmpgf9rssnfjef66f6gh4; _gscu_867320846=35093227ewx2rx38; _gscbrs_867320846=1; loginHistoryRecorded=0; TY_SESSION_ID=029480d3-77c7-48af-b0f0-0edf2d45623c; TRACK_USER_ID=461225; TRACK_IDENTIFY_AT=2018-08-24T06%3A51%3A40.071Z; TRACK_SESSION_ID=7df7fc3cfee9778fe5a8317a72f511fa; TRACK_DETECTED=1.0.1; TRACK_BROWSER_ID=fba350e3683cfa9f188aad89a0cfd5ea; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22461225%22%2C%22%24device_id%22%3A%221656aaff9d460-056137705612f9-34677908-1296000-1656aaff9d5255%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%221656aaff9d460-056137705612f9-34677908-1296000-1656aaff9d5255%22%7D; Hm_lpvt_29d7c655e7d1db886d67d7b9b3846aca=1535201484; Hm_lpvt_b96f95878b55be2cf49fb3c099aea393=1535201485; Hm_lvt_5ff3a7941ce54a1ba102742f48f181ab=1535093500,1535201562; contactMain=1; Hm_lpvt_5ff3a7941ce54a1ba102742f48f181ab=1535245722; username=; rememberusername=; aLastLoginTime=1535263105; _gscs_867320846=t352631017w3d6b10|pv:2',
        'Referer': 'http://chuanbo.weiboyi.com/reform/index',
        'User-Agen': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }

r = requests.get(
    article_top10,
    params=params,
    headers=detail_headers
)

print(r.text)