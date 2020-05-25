import configparser
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import bs4
import re
import datetime

from PIL import Image
import sys
import csv
import logging
import traceback

# local
import mail
import slack

def main():

    config = configparser.ConfigParser()
    config.read('config/config.ini', encoding='utf-8')

    csvList = []
    for i in range(3):
        csvList.extend(getShiftData(config, i))
        
        # printShift(config)

    for row in csvList:
        print(row[0] + "," + row[1])

# 画面遷移しスクリーンショットを保存
def getShiftData(config, placeId):
    
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path=config['CHROME']['PATH'], options=options)
    try:
        driver.get('https://airshift.jp/sft/dailyshift')

        # ログイン画面
        driver.find_element_by_name('username').send_keys(config['AIRSHIFT']['ID'])
        driver.find_element_by_name('password').send_keys(config['AIRSHIFT']['PASS'])
        driver.find_element_by_id('command').submit()

        time.sleep(1)

        # 拠点選択画面
        elements = driver.find_elements_by_class_name('searchTarget')
        elements[placeId].click()

        # デイリーレポート画面
        # 日時指定する場合は、URLを以下などに変更すること
        # https://airshift.jp/sft/dailyshift/20200510
        # 今日
        # https://airshift.jp/sft/dailyshift
        
        url = 'https://airshift.jp/sft/dailyshift'
        
        dayFlg = False
        if len(sys.argv) > 1:
            dayFlg = True
            url = 'https://airshift.jp/sft/dailyshift/' + sys.argv[1]

    
        driver.get(url)
        time.sleep(2)
        select = Select(driver.find_element_by_name('filter-staff'))
        select.select_by_value('fixed')

        driver.find_elements_by_class_name('content___vochnIhs')[0].click()
        page_width = driver.execute_script('return 2500')
        page_height = driver.execute_script('return 2000')
        driver.set_window_size(page_width, page_height)
        time.sleep(2)

        html = driver.page_source
        soup = bs4.BeautifulSoup(html, 'html.parser')

        names = soup.findAll('div',class_="name___1yaaRDba")
        siteList = ["渋谷","難波","新宿"]
        
        csvlist = []
        
        for name in names:
            csvlist.append([name.text.replace('z', '').replace('(AI)', ''),siteList[placeId]])

        driver.save_screenshot(config['AIRSHIFT']['FILE'])
        
        if not dayFlg:
            slack.sendSlack(siteList[placeId])
            
        csvlist = list(map(list, set(map(tuple, csvlist))))

        return csvlist
        
    except Exception as e:
        logging.error(traceback.format_exc())
        return [[]]
    finally:
        driver.quit()

def printShift(config):
    monochrome(config)
    sendGmailAttach(config)

# 画像を白黒化
def monochrome(config):
    img = Image.open(config['AIRSHIFT']['FILE'])
    img_gray = img.convert('L')
    img_gray.save(config['AIRSHIFT']['FILE'])



if __name__ == '__main__':
    main()
