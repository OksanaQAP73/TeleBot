import telebot
from Config import keys, TOKEN
from Extensions import APIException, Crypto


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', ])
def repeat(message: telebot.types.Message):
    text = f'Добро пожаловать, {message.chat.username}!' \
            '\nПоказать инструкцию: /help' \
            '\nЗакончить работу с ботом: /stop'
    bot.reply_to(message, text)


@bot.message_handler(commands=['help', ])
def help_(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате: ' \
           '\n<имя валюты>  <в какую валюту перевести>  <количество переводимой валюты>. ' \
           '\nУвидеть список всех доступных валют:  /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['stop', ])
def stop(message: telebot.types.Message):
    text = f'До новых встреч, {message.chat.username}!'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Введены некорректные параметры')

        quote, base, amount = values
        total_base = Crypto.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {float(total_base) * float(amount):.2f}'
        bot.send_message(message.chat.id, text)


bot.polling()