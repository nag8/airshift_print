siteList = ["渋谷","難波","新宿"]

class Shift:
    def __init__(self, name, placeId, hour):
        # 初期化
        self.name = name
        self.placeId = placeId
        self.hour = hour
        
    def addHour(self, hour):
        self.hour += hour

