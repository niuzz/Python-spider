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
obj = {}
url = 'https://www.uchuanbo.com/member/ajax/news_list.php'
detail_url = 'https://www.uchuanbo.com/member/ajax/mediaaction.php'
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7',
    'Connection': 'close',
    'Content-Length': '150',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': 'PHPSESSID=b29ct75dt3rc3qbi6d94mt2qf4; kefutype=0; Hm_lvt_321dd239bfd0ffe0ed3107c3da888f47=1535106618,1535944466,1536056410,1536630981; ec_im_local_status=0; CUSTOM_INVITE_CONTENT=; ec_invite_state=0; ec_invite_state_time=1536630981575; LXB_REFER=www.google.com; ec_im_tab_num=0; Hm_lpvt_321dd239bfd0ffe0ed3107c3da888f47=1536630987',
    'DNT': '1',
    'Host': 'www.uchuanbo.com',
    'Origin': 'https://www.uchuanbo.com',
    'Referer': 'https://www.uchuanbo.com/member/news.php',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}

folder_path = './images/news-images/'
img_base_url = 'https://www.uchuanbo.com'
proxy = {"http": "http://125.122.18.215:20953"}
save_type = 'excel'
all_news = []

class ucbThread(threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q

    def run(self):
        print("开启线程：" + self.name)
        process_data(self.name, self.q)
        print("退出线程：" + self.name)


def save2Mysql(n_obj):

    sql = "INSERT INTO temp_news_media(`name`, direct_price, `type`, trade_category, district, record_type, send_media, interlinkage_type, `case`, `desc`, home_url)" \
          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    try:
        cursor.execute(sql, (n_obj['name'], n_obj['direct_price'], n_obj['type'], n_obj['trade_category'], n_obj['district'], n_obj['record_type'], n_obj['send_media'], n_obj['interlinkage_type'], n_obj['case'], n_obj['desc'], n_obj['home_url']))
        db.commit()
    except pymysql.InternalError as error:
        code, message = error.args
        print(">>>>>>>>>>>>>", code, message)
        db.rollback()
    print(n_obj)


def save2Excel(index):
    try:
        # workbook = xlwt.Workbook(encoding='utf-8')
        # sheet = workbook.add_sheet('U传播数据', cell_overwrite_ok=True)
        # head = ['名称', '媒体分类', '媒体图片', '备注', '直价', '状态',
        #         '案例', '媒体简介', '媒体类型', '行业分类', '覆盖区域',
        #         '收录参考', '可发媒体', '链接类型', '官网',
        #         '权重', '渠道价格', '编辑收入', '收录率', '入口',
        #         '排序', '媒体详情'
        #         ]  # 表头
        # if index == 1:
        #     for h in range(len(head)):
        #         sheet.write(0, h, head[h])

        rb = open_workbook("./excel/news.xls")
        workbook = copy(rb)
        sheet = workbook.get_sheet(0)

        if index == 0:
            sheet.write(0, 0, '名称')
            sheet.write(0, 1, '媒体分类')
            sheet.write(0, 2, '媒体图片')
            sheet.write(0, 3, '备注')
            sheet.write(0, 4, '直价')
            sheet.write(0, 5, '状态')
            sheet.write(0, 6, '案例')
            sheet.write(0, 7, '媒体简介')
            sheet.write(0, 8, '媒体类型')
            sheet.write(0, 9, '行业分类')
            sheet.write(0, 10, '覆盖区域')
            sheet.write(0, 11, '收录参考')
            sheet.write(0, 12, '可发媒体')
            sheet.write(0, 13, '链接类型')
            sheet.write(0, 14, '官网')
            sheet.write(0, 15, '渠道价格')
            sheet.write(0, 16, '编辑收入')
            sheet.write(0, 17, '收录率')
            sheet.write(0, 18, '入口')
            sheet.write(0, 19, '排序')
            sheet.write(0, 20, '媒体详情')
            workbook.save('./excel/news.xls')

        i = index + 1
        for news in all_news:
            sheet.write(i, 0, news['name'])
            sheet.write(i, 1, '')
            sheet.write(i, 2, news['media_img'])
            sheet.write(i, 3, news['desc'])
            sheet.write(i, 4, news['direct_price'])
            sheet.write(i, 5, '')
            sheet.write(i, 6, news['case'])
            sheet.write(i, 7, '')
            sheet.write(i, 8, news['type'])
            sheet.write(i, 9, news['trade_category'])
            sheet.write(i, 10, news['district'])
            sheet.write(i, 11, news['record_type'])
            sheet.write(i, 12, news['send_media'])
            sheet.write(i, 13, news['interlinkage_type'])
            sheet.write(i, 14, news['home_url'])
            sheet.write(i, 15, '')
            sheet.write(i, 16, '')
            sheet.write(i, 17, '')
            sheet.write(i, 18, '')
            sheet.write(i, 19, '')
            sheet.write(i, 20, '')

            i += 1
        workbook.save('./excel/news.xls')
        print('写入20条excel成功')
    except ValueError:
        print('写入excel失败', ValueError)


def fetch_detail(rel):
    payload = {
        'action': 'viewsmedia',
        'mediaid': rel[0],
        'mediatype': 1,
    }
    r = requests.post(detail_url,
                      data=payload,
                      headers=headers,
                      proxies=proxy)
    r.encoding = 'utf8'
    text = r.text
    try:
        text = json.loads(text)
    except ValueError:
        obj['interlinkage_type'] = ''
        obj['send_media'] = ''

    else:
        text = text['contacthtml']
        soup = BeautifulSoup(text, features="html.parser")
        home_url = soup.find('div', {'class', 'news_p'})
        home_url = home_url.text
        obj['home_url'] = home_url
        table = soup.find('table')
        tds = table.find_all('td')
        obj['interlinkage_type'] = tds[7].text
        obj['trade_category'] = tds[2].text
        str = tds[8].find('em').text
        obj['send_media'] = str

    return obj


def get_detail(tr_list, g_index):
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


        obj['type'] = mid_str
        obj['record_type'] = tds[4].text
        obj['district'] = tds[5].text
        desc = tds[6].text
        obj['desc'] = desc.strip()

        img_origin_url = tds[1].find('div',{'class', 'img'}).find('img')['src']
        fetch_img_url = img_base_url + img_origin_url

        try:
            img_origin_url
        except:
            obj['media_img'] = ''
        else:
            html = requests.get(fetch_img_url, proxies=proxy)
            arr = img_origin_url.split('/')
            face_name = arr[len(arr) -1]
            with open(folder_path + face_name, 'wb') as file:
                file.write(html.content)
                file.flush()
            file.close()
            obj['media_img'] = '/images/news-images/' + face_name

        n_obj = fetch_detail(rel)
        append_obj = obj_copy.deepcopy(n_obj)
        global all_news
        all_news.append(append_obj)
        if len(all_news) % 20 == 0:
            if save_type == 'excel':
                save2Excel(g_index)
            else:
                save2Mysql(n_obj)
            all_news = []



def get_list(page):
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
                      headers=headers,
                      proxies=proxy
                      )
    text = r.text
    text = json.loads(text)
    data = text['datalist']

    soup = BeautifulSoup(data, features="html.parser")
    tr_list = soup.find_all('tr')

    time.sleep(1)
    g_index = page * 20
    get_detail(tr_list, g_index)



# def main():
#     if os.path.exists(folder_path) == False:  # 判断文件夹是否已经存在
#         os.makedirs(folder_path)
#
#     get_list()
#     db.close()
#     print('-------close db-------')
#
#
# if __name__ == '__main__':
#     main()

def process_data(threadName, q):
    if os.path.exists(folder_path) == False:  # 判断文件夹是否已经存在
        os.makedirs(folder_path)

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
workQueue = queue.Queue(500)
threads = []
threadID = 1

# 创建新线程
for tName in range(0, 5):
    thread = ucbThread(threadID, "Thread" + str(tName), workQueue)
    thread.start()
    threads.append(thread)
    threadID += 1

# 填充队列
queueLock.acquire()
for index in range(0, 410):
    # page = index + 1
    workQueue.put(index)
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
