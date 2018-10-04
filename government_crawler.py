import requests
from bs4 import BeautifulSoup as bs
import re

pattern = re.compile(r'\s+')

mother = 'http://www.kocca.kr'
url = 'http://www.kocca.kr/cop/pims/list.do?menuNo=&category=3&recptSt='
req = requests.get(url)
html = req.text

soup = bs(html, 'lxml')
full_list = []
list_num = len(soup.select('#frm > div.board_list_typea.bd_point.bbn > table > tbody > tr'))

full_list.append(soup.select('#frm > div.board_list_typea.bd_point.bbn > table > tbody > tr > td:nth-of-type(1)')[0])
full_list.append(soup.select('#frm > div.board_list_typea.bd_point.bbn > table > tbody > tr > td.tal > a')[0])
full_list.append(soup.select('#frm > div.board_list_typea.bd_point.bbn > table > tbody > tr > td:nth-of-type(3)')[0])
full_list.append(soup.select('#frm > div.board_list_typea.bd_point.bbn > table > tbody > tr > td:nth-of-type(4)')[0])
url = full_list[1].get('href')


result = []
value_list = []
text_list = ['사업번호', '제목', '등록일', '접수기간']
for texts in full_list:
    sentence = re.sub(pattern, '', texts.text)
    value_list.append(sentence)
for i in range(4):
    result.append(text_list[i] + ' : ' + value_list[i])
result.append('URL : ' + url)

print(result)
