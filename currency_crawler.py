import urllib.request
from bs4 import BeautifulSoup
import chatbot_currency

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

currency_target = ['미국 USD', '유럽연합 EUR', '일본 JPY (100엔)', '중국 CNY', '홍콩 HKD', '대만 TWD']

for key in money_data:
    if key in currency_target:
        value = money_data.get(key)
        chatbot_currency.send_currency(key, value)
    else:
        pass
