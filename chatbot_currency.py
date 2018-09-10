import telegram
from datetime import datetime

my_token = '620119228:AAFzcyGBnMYRxh22--x3_WprBVODyTdIcok'
chatbot = telegram.Bot(token = my_token)
chat_id = -1001289433156
#chat_id = chatbot.getUpdates()[-1].message.chat.id

now = datetime.now()
chatbot.sendMessage(chat_id=chat_id, text='***오늘 '+ str('%s-%s-%s' % ( now.year, now.month, now.day )) + '의 환율은 다음과 같습니다.***')

def send_currency(currency, value):
   chatbot.sendMessage(chat_id = chat_id, text = '현재 ' + currency + ' 환율은 ' + str(value) + '원입니다')