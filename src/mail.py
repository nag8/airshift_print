import configparser
from smtplib import SMTP
from email.mime.text import MIMEText
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

def sendGmailAttach(config):
    sender, password = config['MAIL']['ID'], config['MAIL']['PASS']
    host, port = 'smtp.gmail.com', 587

    msg = MIMEMultipart()
    msg['Subject'] = 'Airシフト印刷'
    msg['From'] = sender
    msg['To'] = config['MAIL']['TO']
    msg.attach(MIMEText('本文'))

    # 添付ファイルの設定
    attach_file = {'name': 'airshift.png', 'path': config['AIRSHIFT']['FILE']}
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
