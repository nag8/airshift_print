import requests
import json
import configparser
import slackweb

import util

def sendSlack(fileName):
    
    config = util.getConfig()

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

def post(url='', text=''):

    payload_dic = {
        'text' : text
    }

    requests.post(url, data=json.dumps(payload_dic))
    
    
if __name__ == '__main__':
    post(
        '<@UMTN0H3DG> aaqaa'
    )
