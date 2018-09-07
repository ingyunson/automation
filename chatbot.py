import telegram

bot = telegram.Bot(token = '568355082:AAEVrHrZdV-R1Pv6jT5Y_VD3GJe9N1EUIg0')
chat_id = bot.getUpdates()[-1].message.chat.id
name = input()
bot.sendMessage(chat_id = chat_id, text = chat_id)
bot.sendMessage(chat_id = chat_id, text = 'hello' + name)

