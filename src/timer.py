import datetime
import schedule
import time
import main

def job():
  main.main()

schedule.every().day.at("08:30").do(job)

while True:
  schedule.run_pending()
  time.sleep(60)
