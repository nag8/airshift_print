import configparser
from datetime import datetime, timedelta

def getConfig():
    config = configparser.ConfigParser()
    config.read('config/config.ini', encoding='utf-8')
    return config

def judgeToday(num):
    today = datetime.now()
    t = datetime(1899, 12, 30) + timedelta(days=int(num))
    if today.year == t.year and today.month == t.month and today.day == t.day:
        return True
    
    return False

