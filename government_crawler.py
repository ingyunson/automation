import requests
from bs4 import BeautifulSoup as bs
import re

pattern = re.compile(r'\s+')

mother = 'http://www.kocca.kr'
url = 'http://www.kocca.kr/cop/pims/list.do?menuNo=&recptSt='
req = requests.get(url)
html = req.text

soup = bs(html, 'lxml')
full_list = []
list_num = len(soup.select('#frm > div.board_list_typea.bd_point.bbn > table > tbody > tr'))

for i in range(list_num):
    list = []
    target = soup.select('#frm > div.board_list_typea.bd_point.bbn > table > tbody > tr:nth-of-type(' + str(i + 1) + ')')[0]
    title = target.select('td:nth-of-type(2) > a')[0]
    for num in range(1, 5):
        texts = target.select('td:nth-of-type(' + str(num) +')')[0]
        sentence = re.sub(pattern, '', texts.text)
        list.append(sentence)
    list.append(title.get('href'))
    full_list.append(list)

result = []
text_list = ['사업번호', '제목', '등록일', '접수기간', 'URL']

for idx in range(len(full_list)):
    target = full_list[idx]
    result.append('INDEX = ' + str(idx))
    for i in range(4):
        result.append(text_list[i] + ' : ' + full_list[idx][i])
    result.append(text_list[4] + ' : ' + mother + full_list[idx][4])
    result.append('\n')

print('\n'.join(result))
