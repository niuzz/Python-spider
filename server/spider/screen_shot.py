from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import json


class Screen_Shot(object):
    def __init__(self):
        pass

    def run(self, keyword, aid):
        begin = time.time()
        driver = self.get_chrome()
        result = self.get_screen_shot(driver, keyword, aid)
        total = time.time() - begin
        return result

    def get_chrome(self):
        window_size = ('700', '500')
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.set_window_size(*window_size)
        return driver

    def get_screen_shot(self, driver, keyword, aid):
        # 新闻源收录
        driver.get("https://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&word=%s" % keyword)
        time.sleep(3)
        elem = driver.find_elements_by_class_name("result")
        if len(elem) > 1:
            return None
        else:
            if elem:
                img_url = self.run_js(driver, aid)
                return json.dumps({'aid': aid, 'type': 'news', 'img_url': img_url})
            # 网页收录
            else:
                driver.get("https://www.baidu.com/s?&wd=%s&ie=utf-8" % keyword)
                elem = driver.find_elements_by_class_name("result")
                if elem:
                    img_url = self.run_js(driver, aid)
                    return json.dumps({'aid': aid, 'type': 'web', 'img_url': img_url})
                else:
                    return None
                    pass

    def run_js(self, driver, aid):
        driver.execute_script(
            """
            (function(){
                  var result = document.querySelector('.result')
                  if(result) {
                    result.setAttribute('style','border:5px solid red;padding:10px;margin-left:-15px')
                  } else {}
            })()
            """
        )
        file_name = aid + '_' + str(self.now_time())
        driver.save_screenshot('./images/%s.png' % file_name)
        return '/images/%s.png' % file_name

    def now_time(self):
        t = time.time()
        get_time = lambda: int(round(t * 1000))
        return get_time()
