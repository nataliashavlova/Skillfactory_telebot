import telebot
from config import keys, TOKEN
from extensions import APIException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Приветствую!\nЧтобы начать работу, введите через пробел с маленькой буквы следующие параметры: \n1) имя валюты, стоимость которой вас интересует\n\
2) имя валюты, в которую нужно перевести стоимость первой указанной валюты\n\
3) количество переводимой (первой) валюты\n\nПример: доллар рубль 10\n\nУвидеть список всех доступных валют можно по команде /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Список доступных валют:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Количество вводимых параметров должно равняться трём.')

        base, quote, amount = values
        total_base = CurrencyConverter.get_price(base, quote, amount)
        base_price = total_base / float(amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        text = f'Цена {amount} {base} в {quote} = {total_base}.\n\
(при текущей стоимости 1 {base}, равной {base_price} {quote})'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)