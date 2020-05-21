import datetime
import schedule
import time
import shift

def job():
  shift.main()



schedule.every().day.at("08:30").do(job)
  
while True:
  schedule.run_pending()
  time.sleep(60)
