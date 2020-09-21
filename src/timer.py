import datetime
import schedule
import time
import main
import util

def shift():
    main.shift()

def duty():
    if not util.judgeFriday():
        main.duty()

schedule.every().day.at("08:30").do(shift)
schedule.every().day.at("10:00").do(duty)

while True:
    schedule.run_pending()
    time.sleep(60)
