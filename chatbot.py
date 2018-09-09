from telegram.ext import Updater, MessageHandler, Filters, CommandHandler

my_token = '568355082:AAEVrHrZdV-R1Pv6jT5Y_VD3GJe9N1EUIg0'
#chatbot = telegram.Bot(token = '568355082:AAEVrHrZdV-R1Pv6jT5Y_VD3GJe9N1EUIg0')
#chat_id = chatbot.getUpdates()[-1].message.chat.id

#chatbot.sendMessage(chat_id = chat_id, text = chat_id)
#chatbot.sendMessage(chat_id = chat_id, text = 'hello')

print('starting telegram bot')

def get_message(bot, update) :
    update.message.reply_text('got Text') #'got text'를 답장
    update.message.reply_text(update.message.text) #받은 메시지를 답장

def help_command(bot, update) :
    update.message.reply_text("무엇을 도와드릴까요?")

updater = Updater(my_token) #my_token에 업데이트된 사항이있으면 가져옴

message_handler = MessageHandler(Filters.text, get_message) #텍스트에 반응하여 get_message 함수를 호출
updater.dispatcher.add_handler(message_handler) #updater에 message_handler를 더해줌

help_handler = CommandHandler('help', help_command) #help 명령에 반응하여 help_command 함수를 호출
updater.dispatcher.add_handler(help_handler)

updater.start_polling(timeout = 3, clean = True) #polling 시작
updater.idle() #updater가 종료되지 않고 계속 실행되고 있도록