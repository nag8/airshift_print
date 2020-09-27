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
import util


def shift():

    config = util.getConfig()

    shiftlist = []
    getShiftData(config, 3)

        # printShift(config)

    for s in shiftlist:

        print(s.name, s.placeId, s.hour)

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
        page_height = driver.execute_script('return 4000')
        driver.set_window_size(page_width, page_height)
        time.sleep(2)

        html = driver.page_source
        soup = bs4.BeautifulSoup(html, 'html.parser')

        names = soup.findAll('div',class_="name___1yaaRDba")
        siteList = ["渋谷","難波","新宿","拠点統合"]
        
        csvlist = []
        
        for name in names:
            csvlist.append([name.text.replace('z', '').replace('(AI)', ''),siteList[placeId]])

        driver.save_screenshot(config['AIRSHIFT']['FILE'])
        
        # if not dayFlg:
        #     slack.sendSlack(siteList[placeId])
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


def getTime(str):
    return dt.timedelta(hours=int(str[:2]), minutes=int(str[-3:-1]))


def duty():
    config = util.getConfig()
    dutyList = gsheet.getTodayDuty()
    mentionList = gsheet.getMentionList()
    
    # 打刻当番
    # message = '本日の申請確認担当は<@' + util.getMention(mentionList, dutyList[0]) + '>です。'\
    # '\n当日、10時までの申請分について対応してください。'\
    # '\nマニュアル：https://infratop.docbase.io/posts/1538760'

    # slack.post(url=config['SLACK']['URL_ST'], text=message)
    
    # その他
    message = '本日の当番です！'\
        '\n学サポ日直　：<@' + util.getMention(mentionList, dutyList[0]) + '>'\
        '\nメンサポ日直：<@' + util.getMention(mentionList, dutyList[1]) + '>'\
        '\n昼会司会　　：<@' + util.getMention(mentionList, dutyList[2]) + '>'

    slack.post(url=config['SLACK']['URL_LSI'], text=message)


if __name__ == '__main__':
    duty()
