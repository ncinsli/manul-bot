from telebot import *
import re
import os

bot = TeleBot(token=os.environ["MANUL_BOT"])
bot.parse_mode = 'html'

def get_last():
    with open('manuls.dat', 'r') as f:
        last = int(f.read())
    return last

def set_last(last):
    with open('manuls.dat', 'w') as f:
        f.write(str(last))

@bot.message_handler(commands=['init'])
def init(message):
    if len(message.text.split()) == 1: 
        bot.send_message(message.chat.id, '❌  Введите последнего подсчитанного манула!\nПример: /init 20030')
        return 
    
    bot.send_message(message.chat.id, '🐱  Подсчёт манулов активирован!')
    set_last(int(message.text.split()[1]))


@bot.message_handler(commands=['stat'])
def stat(message):
    bot.reply_to(message, '⚙  Статистика\n\nМанулов сейчас: ' + str(get_last()))

@bot.message_handler()
def on_message(message):
    raw = message.text
    number = re.sub("[^0-9]", "", raw)
    if number == '': return

    number = int(number)

    if number - get_last() == 1:
        set_last(number)
    else: 
        bot.reply_to(message, '❌  Порядок манулов нарушен <pre>' + str(get_last() + 1) + '</pre>')

bot.infinity_polling()