import configparser
import csv
import mentor
import work
import datetime


def  main():
    
    config = configparser.ConfigParser()
    config.read('config/config.ini', encoding='utf-8')
    
    mentorList = []
    
    with open(config['CSV']['IN']) as f:
        reader = csv.reader(f)
        days = next(reader)
        l = [row for row in reader]
        
    days.pop(0)
    
    for row in l:
        name = row.pop(0).replace('z', '').replace('(AI)', '')
        
        duplicationFlg = False
        for m in mentorList:
            if name == m.name:
                duplicationFlg = True
                for i in range(len(m.workList)):
                    m.workList[i].setTime(row[i])
                break
                
        if not duplicationFlg:
            m = mentor.Mentor(name = name, placeId = 0, workList = [])
            m.initWorkList(days)
            for i in range(len(row)):
                m.workList[i].setTime(row[i])
                
            mentorList.append(m)
        
    # for j in mentorList[4].workList:
        # print(j.startTime)
        # print(mentorList[0].workList)
    
def setWork(m, row):
    for i in range(len(row)):
        if row[i] == '':
            continue
        else:
            m.workList[i].startTime = 999
            m.workList[i].endTime = 999
            


if __name__ == '__main__':
    main()
