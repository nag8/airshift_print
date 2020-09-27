import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials

import util


def prepare(config):
    # 2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    # 認証情報設定
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        config['GOOGLE']['JSON'], scope)
    return gspread.authorize(credentials)


def getWks(sheetName):

    config = util.getConfig()
    gc = prepare(config)

    return gc.open_by_key(config['GOOGLE']['SPREADSHEET']).worksheet(sheetName)


def getSS():

    config = util.getConfig()
    gc = prepare(config)

    return gc.open_by_key(config['GOOGLE']['SPREADSHEET'])


def getTodayDuty():

    ss = getSS()
    dataList = ss.values_get(
        '当番!A:G', params={'valueRenderOption': 'FORMULA'})['values']
    dataList.pop(0)
    dataList.pop(0)

    for row in dataList:
        if util.judgeToday(row[0]):
            return [row[4], row[5], row[6]]
    return 'error'


def getMentionList():
    wks = getWks('メンバー')
    return wks.get_all_values()



if __name__ == '__main__':

    print(getTodayDuty())
