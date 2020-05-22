import requests
import json
import configparser

def sendSlack(fileName):
    
    config = configparser.ConfigParser()
    config.read('config/config.ini', encoding='utf-8')

    files = {'file': open(config['AIRSHIFT']['FILE'], 'rb')}
    param = {
        'token'    : config['SLACK']['TOKEN'],
        'channels' : config['SLACK']['CHANNEL'],
        'initial_comment' : fileName
    }
    res = requests.post(
        url="https://slack.com/api/files.upload",
        params=param, 
        files=files)


if __name__ == '__main__':
    sendSlack('神南')
