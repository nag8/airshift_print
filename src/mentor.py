import work
siteList = ["渋谷","難波","新宿"]

class Mentor:
    def __init__(self, name, placeId, workList):
        # 初期化
        self.name = name
        self.placeId = placeId
        self.workList = workList
    
    def initWorkList(self, l):
        for d in l:
            self.workList.append(work.Work(day = d))
