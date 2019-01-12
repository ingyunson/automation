import urllib.request
from bs4 import BeautifulSoup

def currency_get():
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
    return money_data

