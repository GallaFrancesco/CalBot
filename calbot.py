from telegram.ext import Updater, CommandHandler
from time import sleep
from datetime import datetime
import subprocess
import schedule

def relay_timetable (update, msg, tomorrow):
    print ("Sending timetable!")
    if tomorrow:
        apts = subprocess.check_output(['calcurse','-d', '2']).decode('utf-8').split("\n\n")
        apt = apts[1]
    else:
        apt = subprocess.check_output(['calcurse','-a']).decode('utf-8')
    update.message.reply_text(msg)
    update.message.reply_text(apt)
    print ('[A] '+ apt)

def start(bot, update):
    print('[B] Bot started')
    update.message.reply_text('I will provide you the CalCurse timetable for each working day.')
    schedule.every().day.at("21:00").do(relay_timetable, update, "Tomorrow's appointments", True)
    schedule.every().day.at("8:00").do(relay_timetable, update, "Today's appointments", False)
    while True:
        print ('[B] Is it 9 yet?')
        schedule.run_pending()
        sleep(60)

updater = Updater('your token here')
updater.dispatcher.add_handler(CommandHandler('start', start))

updater.start_polling()
updater.idle()
