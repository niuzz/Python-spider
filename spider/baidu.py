from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time

window_size = ('1440', '1600')
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.set_window_size(*window_size)
driver.get("https://www.baidu.com/")

elem = driver.find_element_by_name("wd")

elem.send_keys("chinabyte")
elem.send_keys(Keys.RETURN)

time.sleep(3)
print(driver.page_source)
driver.save_screenshot('1.png')
