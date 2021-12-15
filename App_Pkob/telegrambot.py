#from _curses import echo
import telegram
import django
import os
os.environ['DJANGO_SETTINGS_MODULE']= 'PKOB.settings'
django.setup()
import datetime
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters, ConversationHandler
from App_Pkob.models import People
bot = telegram.Bot(token='5048441785:AAFabkWFfpMjXFIkw9ek0G1xuIwrTuGXtDY')

updater = Updater('5048441785:AAFabkWFfpMjXFIkw9ek0G1xuIwrTuGXtDY', use_context=True)
dispatcher = updater.dispatcher
Ic, Phone = range(2)
print("test")
msgphone = ''


def start(update:updater, context: CallbackContext):
    print('starting')
    update.message.reply_text("hello,welcome to the pkob bot")
    update.message.reply_text("Please enter your ic number ")
    return Ic


def ic(update: updater, context: CallbackContext):
    global msgic
    msgic = update.message.text
    if not People.objects.filter(IcNo=msgic).exists():
        update.message.reply_text("IC number entered does not exist in our records,Please reenter your IC number  ")
        return Ic
    else:
        print("ic :", msgic)
        update.message.reply_text("Please enter your phone number  ")
        return Phone


def phone(update:updater, context: CallbackContext):
    msgphone = update.message.text
    print("phone :", msgphone)
    print("icno :", msgic)
    if not People.objects.filter(Phone=msgphone).exists():
        update.message.reply_text("Phone number entered does not exist in our records,Please reenter your phone number ")
        return Phone
    else:
        update.message.reply_text("Done ")
        user_input(msgic, msgphone, update)
        return ConversationHandler.END


def user_input(icno, phoneno , update: updater):

    if People.objects.filter(IcNo=icno).exists() and People.objects.filter(Phone=phoneno).exists():
        person = People.objects.get(IcNo=icno)
        phone_num = person.Phone
        print("ic ", person.IcNo)
        icNum = person.IcNo
        print("Phone ", phone_num)
        full_name = person.Name
        print("Name ", full_name)
        cal_age = calculateage(person.IcNo)
        print("Age", cal_age)
        result=("kad Pengenalan: " + icNum + "\nNombor Telefon: " +
                                  phone_num + "\nNama: " + full_name + "\nUmur: " + str(cal_age))
        update.message.reply_text(result)
    else:
        return update.message.reply_text("User does not exist ")



def calculateage(ic):
        current = datetime.datetime.now().year
        test = ic[-4]
        year=''
        if test == "0":
           year =(("20" + str(ic)[:2]).replace(",", ""))
           print(year)
        elif test == '5' or test == "6" or test == '7':
            year=(("19" + str(ic)[:2]).replace(",", ""))

        age = current - int(year)
        print(age)
        return age


def done(update: updater, context: CallbackContext):
    update.message.reply_text("Thank you ")


conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        Ic: [MessageHandler(filters=None, callback=ic)],
        Phone: [MessageHandler(filters=None, callback=phone)],

    },
    fallbacks=[CommandHandler("Done", done)]
)
dispatcher.add_handler(conv_handler)


updater.start_polling()
updater.idle()
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

