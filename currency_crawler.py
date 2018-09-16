import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime
import telegram

my_token = '620119228:AAFzcyGBnMYRxh22--x3_WprBVODyTdIcok' #botfather로 받은 토큰
chatbot = telegram.Bot(token = my_token)
chat_id = '@currencybot2018' #채널의 경우 @채널주소

fp = urllib.request.urlopen('http://info.finance.naver.com/marketindex/exchangeList.nhn')
source = fp.read()
fp.close()
class_list = ["tit", "sale"]
soup = BeautifulSoup(source, 'html.parser')
soup = soup.find_all("td", class_=class_list)
money_data = {}
for data in soup:
    if soup.index(data) % 2 == 0:
        data = data.get_text().replace('\n', '').replace('\t', '')
        money_key = data
    elif soup.index(data) % 2 == 1:
        money_value = data.get_text()
        money_data[money_key] = money_value
        money_key = None
        money_value = None

now = datetime.now()
currency_target = ['미국 USD', '유럽연합 EUR', '일본 JPY (100엔)', '중국 CNY', '홍콩 HKD', '대만 TWD']
message = ['***오늘 '+ str('%s-%s-%s' % (now.year, now.month, now.day + 1)) + '의 환율은 다음과 같습니다.***']

for key in money_data:
    if key in currency_target:
        value = money_data.get(key)
        message.append(key + '의 환율은 ' + str(value) + '원입니다.')
    else:
        pass

text = "\n".join(message)

chatbot.sendMessage(chat_id = chat_id, text = text)