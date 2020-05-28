import datetime
siteList = ["渋谷","難波","新宿"]

class Work:
    def __init__(self, day, workFlg=False, startTime=None, endTime=None):
        # 初期化
        self.day = day
        self.workFlg = workFlg
        self.startTime = startTime
        self.endTime = endTime
        
    def setTime(self, timeStr):
        if timeStr != '':
            self.workFlg = True
            start, end = timeStr.split('〜')
            start = datetime.datetime.strptime(start, '%H:%M')
            end = datetime.datetime.strptime(end, '%H:%M')
            
            if self.startTime is None or self.startTime > start:
                self.startTime = start
                
            if self.endTime is None or self.endTime < end:
                self.endTime = end
