import yaml
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select

from PIL import Image
import sys

print('start...')

driver = webdriver.Chrome()
driver.get('https://airshift.jp/sft/dailyshift')

with open('../config/config.yml') as file:
    config = yaml.load(file, Loader=yaml.SafeLoader)

# ログイン画面
driver.find_element_by_name('username').send_keys(config['ID'])
driver.find_element_by_name('password').send_keys(config['PASS'])
driver.find_element_by_id('command').submit()

time.sleep(1)

# 拠点選択画面
elements = driver.find_elements_by_class_name('searchTarget')
elements[config['SITE']].click()

# デイリーレポート画面
driver.get('https://airshift.jp/sft/dailyshift')
time.sleep(2)
select = Select(driver.find_element_by_name('filter-staff'))
select.select_by_value('fixed')

driver.find_elements_by_class_name('root___1ZI4hW8s')[0].click()
time.sleep(2)
driver.save_screenshot(config['FILE'])

driver.quit()

# 画像を白黒化
img = Image.open(config['FILE'])
img_gray = img.convert('L')
img_gray.save(config['FILE'])

print('finish!')
