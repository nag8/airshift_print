import yaml
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select

from PIL import Image
import sys
import subprocess

from smtplib import SMTP
from email.mime.text import MIMEText
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

def main():
    print('start...')

    with open('../config/config.yml') as file:
        config = yaml.load(file, Loader=yaml.SafeLoader)
    
    getScreenShot(config)

    # monochrome(config)
    # sendGmailAttach(config)
    sendSlack(config)
    print('finish!')

# 画面遷移しスクリーンショットを保存
def getScreenShot(config):

    
    driver = webdriver.Chrome()
    driver.get('https://airshift.jp/sft/dailyshift')

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

    driver.find_elements_by_class_name('content___vochnIhs')[0].click()
    time.sleep(2)

    driver.save_screenshot(config['FILE'])
    print("take photo")
    time.sleep(20)

    driver.quit()

# 画像を白黒化
def monochrome(config):
    img = Image.open(config['FILE'])
    img_gray = img.convert('L')
    img_gray.save(config['FILE'])


def sendGmailAttach(config):
    sender, password = config['MAIL_ID'], config['MAIL_PASS']
    host, port = 'smtp.gmail.com', 587

    msg = MIMEMultipart()
    msg['Subject'] = 'Airシフト印刷'
    msg['From'] = sender
    msg['To'] = config['MAIL_TO']
    msg.attach(MIMEText('本文'))

    # 添付ファイルの設定
    attach_file = {'name': 'airshift.png', 'path': config['FILE']}
    attachment = MIMEBase('image', 'png')

    file = open(attach_file['path'], 'rb+')
    attachment.set_payload(file.read())
    file.close()

    encoders.encode_base64(attachment)
    attachment.add_header("Content-Disposition", "attachment", filename=attach_file['name'])
    msg.attach(attachment)

    # gmailへ接続(SMTPサーバーとして使用)
    gmail=SMTP("smtp.gmail.com", 587)
    gmail.starttls()
    gmail.login(sender, password)
    gmail.send_message(msg)

def sendSlack(config):
    subprocess.call(["slackcat", "--channel", config['SLACK_CHANNEL'], "--filename","シフト.png", config['FILE']])

if __name__ == '__main__':
    main()
