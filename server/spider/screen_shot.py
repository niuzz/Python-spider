from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


class Screen_Shot(object):
    def __init__(self):
        pass

    def run(self, keyword):
        begin = time.time()
        driver = self.get_chrome()
        result = self.get_screen_shot(driver, keyword)
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

    def get_screen_shot(self, driver, keyword):
        # 新闻源收录
        driver.get("https://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&word=%s" % keyword)
        time.sleep(3)
        elem = driver.find_elements_by_class_name("result")
        if len(elem) > 1:
            return '匹配不精确'
        if elem:
            self.run_js(driver)
            return 'file-ok'
        # 网页收录
        else:
            driver.get("https://www.baidu.com/s?&wd=%s&ie=utf-8" % keyword)
            elem = driver.find_elements_by_class_name("result")
            if elem:
                self.run_js(driver)
                return 'file-ok'
            else:
                return '没有收录'
                pass

    def run_js(self, driver):
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
        driver.save_screenshot('1.png')
