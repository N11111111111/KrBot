
import telebot
from config import keys, keys_base, TOKEN, access_key
from extensions import ConvertionException, CriptoConverter


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands = ['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Вас приветствует бот конвертации валют! \ Чтобы начать работу введите комманду боту в следующем формате: \n первая валюта  - <доллар> \
<в какую валюту перевести> \
<количество переводимой валюты>\n Что бы увидеть список всех доступных валют нaжмите:/values'
    bot.reply_to(message, text)


@bot.message_handler(commands = ['values'])
def values(message: telebot.types.Message):
    keys.update(keys_base)
    text = 'Базовая валюта  - доллар.\n Доступные валюты для перевода:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text    )


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
   try:
        values = message.text.split(" ")
        if len(values) != 3:
            raise ConvertionException('У Вас написано не три параметра')

        base, symbols, amount = values
        total_base = CriptoConverter.get_price(base, symbols, amount)

   except ConvertionException as e:
       bot.reply_to(message, f'Ошибка пользователя.\n{e}')

   except ConvertionException  as e:
       bot.reply_to(message, f'Не удалось обработать команду\n{e}')

   else:
    text = f'{amount} {base} стоит {total_base} {symbols}'
    bot.send_message(message.chat.id, text)

bot.polling()


