import telegram
from datetime import datetime

my_token = '620119228:AAFzcyGBnMYRxh22--x3_WprBVODyTdIcok' #botfather로 받은 토큰
chatbot = telegram.Bot(token = my_token)
chat_id = '@currencybot2018' #채널의 경우 @채널주소

now = datetime.now()
chatbot.sendMessage(chat_id=chat_id, text='***오늘 '+ str('%s-%s-%s' % ( now.year, now.month, now.day )) + '의 환율은 다음과 같습니다.***')

def send_currency(currency, value):
    chatbot.sendMessage(chat_id = chat_id, text = '현재 ' + currency + ' 환율은 ' + str(value) + '원입니다')