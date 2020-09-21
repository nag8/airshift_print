import configparser
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import bs4
import re
import datetime as dt

from PIL import Image
import sys
import csv
import logging
import traceback

# local
import mail
import slack
import shift
import gsheet

def shift():

    config = configparser.ConfigParser()
    config.read('config/config.ini', encoding='utf-8')

    shiftlist = []
    for i in range(1):
        shiftlist.extend(getShiftData(config, i))
        
        # printShift(config)

    for s in shiftlist:
        
        print(s.name, s.placeId, s.hour)

# 画面遷移しスクリーンショットを保存
def getShiftData(config, placeId):
    
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    
    if 'CHROME' in config:
        driver = webdriver.Chrome(executable_path=config['CHROME']['PATH'], options=options)
    else:
        driver = webdriver.Chrome(options=options)
        
    shiftlist = []
    
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

        siteList = ["渋谷","難波","新宿"]
        
        driver.save_screenshot(config['AIRSHIFT']['FILE'])
        
        if dayFlg:
            html = driver.page_source
            soup = bs4.BeautifulSoup(html, 'html.parser')
            names = soup.findAll('div',class_="name___1yaaRDba")
            
            for name in names:
                hour = getTime(name.parent.find("div", attrs={"class": "worktime___1N2NXLC5"}).span.text)
                name = name.text.replace('z', '').replace('(AI)', '')
                
                uniqueFlg = True
                
                for s in shiftlist:
                    if name == s.name:
                        s.addHour(hour)
                        uniqueFlg = False
                        
                
                if uniqueFlg:
                    shiftlist.append(
                        shift.Shift(
                            name = name,
                            placeId = placeId,
                            hour = hour
                        )
                    )
        else:
            slack.sendSlack(siteList[placeId])

        return shiftlist
        
    except Exception as e:
        logging.error(traceback.format_exc())
        return shiftlist
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
    
def getTime(str):
    return dt.timedelta(hours = int(str[:2]), minutes = int(str[-3:-1]))

def duty():
    dutyList = gsheet.getTodayDuty()
    

if __name__ == '__main__':
    duty()
