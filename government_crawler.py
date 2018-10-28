import requests
from bs4 import BeautifulSoup as bs
import re

pattern = re.compile(r'\s+')


def parse(url):
    req = requests.get(url)
    html = req.text
    soup = bs(html, 'lxml')

    return soup

def kocca() :
    kocca_mother = 'http://www.kocca.kr'
    kocca_url = 'http://www.kocca.kr/cop/pims/list.do?menuNo=&recptSt='
    soup = parse(kocca_url)

    full_list = []
    list_num = len(soup.select('#frm > div.board_list_typea.bd_point.bbn > table > tbody > tr'))

    try:
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
    except:
        Error = 'Error occurs, please check the URL\nURL : ' + kocca_url + '\n'
        return Error

    result = []
    result.append('##### 콘텐츠진흥원 지원사업 #####' + '\n')
    text_list = ['사업번호', '제목', '등록일', '접수기간', 'URL']

    for idx in range(len(full_list)):
        target = full_list[idx]
        result.append('INDEX = ' + str(idx))
        for i in range(4):
            result.append(text_list[i] + ' : ' + target[i])
        result.append(text_list[4] + ' : ' + kocca_mother + target[4])
        result.append('\n')
    output = '\n'.join(result)
    return output

def kpipa_business():
    business_url = 'http://www.kpipa.or.kr/info/tenderList.do?board_id=157'
    soup = parse(business_url)

    full_list = []
    key = ['번호', '제목', '등록일']
    list_num = len(soup.select('#contents > div.tblWrap > table > tbody > tr'))

    for i in range(list_num):
        target = soup.select('#contents > div.tblWrap > table > tbody > tr:nth-of-type(' + str(i + 1) + ') > td')
        title = target[2]
        list = []
        for num in [0, 2, 3]:
            texts = target[num].text
            list.append(texts)
        full_list.append(list)

    result = []
    result.append('##### 출판문화산업진흥원 외부입찰 #####')
    result.append('사이트 주소 : ' + business_url + '\n')
    for idx in range(len(full_list)):
        target = full_list[idx]
        result.append('INDEX = ' + str(idx))
        for i in range(3):
            result.append(key[i] + ' : ' + target[i])
        result.append('\n')
    output = '\n'.join(result)

    return output


def kpipa_give():
    give_url = 'http://www.kpipa.or.kr/info/newsList.do?board_id=1'
    soup = parse(give_url)

    full_list = []
    key = ['번호', '제목', '등록일']
    list_num = len(soup.select('#contents > div.tblWrap > table > tbody > tr'))

    for i in range(list_num):
        target = soup.select('#contents > div.tblWrap > table > tbody > tr:nth-of-type(' + str(i + 1) + ') > td')
        title = target[2]
        list = []
        for num in [0, 2, 3]:
            texts = target[num].text
            list.append(texts)
        full_list.append(list)

    result = []
    result.append('##### 출판문화산업진흥원 지원사업 #####')
    result.append('사이트 주소 : ' + give_url + '\n')
    for idx in range(len(full_list)):
        target = full_list[idx]
        result.append('INDEX = ' + str(idx))
        for i in range(3):
            result.append(key[i] + ' : ' + target[i])
        result.append('\n')
    output = '\n'.join(result)

    return output

