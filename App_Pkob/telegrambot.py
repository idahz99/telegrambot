import django
import os
from App_Pkob.config import TOKEN,PORT
os.environ['DJANGO_SETTINGS_MODULE']= 'PKOB.settings'
django.setup()
import datetime
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters, ConversationHandler
from App_Pkob.models import People
import logging
updater = Updater(TOKEN)

dispatcher = updater.dispatcher
Ic, Phone = range(2)
print("test")
print(PORT)
print(TOKEN)
msgphone = ''


def start(update: updater,context):
    print('starting')
    update.message.reply_text("hello,welcome to the pkob bot")
    update.message.reply_text("Please enter your ic number ")
    return Ic


def ic(update: updater,context):
    global msgic
    msgic = update.message.text
    if msgic == "/cancel":
        update.message.reply_text("Process cancelled ,Thank you ")
        return ConversationHandler.END
    elif not People.objects.filter(IcNo=msgic).exists():
        update.message.reply_text("IC number entered does not exist in our records,Please try again")
        return Ic
    else:
        print("ic :", msgic)
        update.message.reply_text("Please enter your phone number  ")
        return Phone


def phone(update: updater,context):
    msgphone = update.message.text
    print("phone :", msgphone)
    print("icno :", msgic)
    test = People.objects.get(IcNo=msgic)
    if msgphone == "/cancel":
        update.message.reply_text("Process cancelled ,Thank you ")
        return ConversationHandler.END
    elif not People.objects.filter(Phone=msgphone).exists():
        update.message.reply_text("Phone number entered does not exist in our records,Please try again")
        return Phone
    elif not test.Phone == msgphone:
        update.message.reply_text("Incorrect phone number")
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
        year = ''
        if test == "0":
            year = (("20" + str(ic)[:2]).replace(",", ""))
            print(year)
        elif test == '5' or test == "6" or test == '7':
            year = (("19" + str(ic)[:2]).replace(",", ""))

        age = current - int(year)
        print(age)
        return age


def done(update: updater):
    update.message.reply_text("Thank you ")
    return ConversationHandler.END


conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        Ic: [MessageHandler(filters=None, callback=ic)],
        Phone: [MessageHandler(filters=None, callback=phone)],

    },
    fallbacks=[CommandHandler("cancel", done)]
)
dispatcher.add_handler(conv_handler)



updater.start_polling()
updater.idle()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

