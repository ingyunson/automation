import telegram
from government_crawler import kocca, kpipa_business, kpipa_give
from datetime import datetime

my_token = '<TOKEN_ADDRESS>' #botfather로 받은 토큰
chatbot = telegram.Bot(token = my_token)
chat_id = '<ITELEGRAM_ID_NUM>' #채널의 경우 @채널주소

now = datetime.now()

chatbot.sendMessage(chat_id=chat_id, text=kocca())
chatbot.sendMessage(chat_id=chat_id, text=kpipa_business())
chatbot.sendMessage(chat_id=chat_id, text=kpipa_give())

