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
    kocca_url = 'http://www.kocca.kr/cop/pims/list.do?menuNo=200828&recptSt='
    kocca = 'http://www.kocca.kr'
    soup = parse(kocca_url)

    full_list = []
    list_num = len(soup.select('#frm > div.board_list.mt25 > div.board_list_body > div > div.subject > a'))

    try:
        for i in range(list_num):
            list = []
            target = soup.select('#frm > div.board_list.mt25 > div.board_list_body > div')[0]
            title = target.select('div.subject > a')[0]
            sub_url = title.get('href')
            target_url = kocca + sub_url

            target_num = target.select('div:nth-of-type(1)')[0].text
            target_title = title.text.strip()
            target_date = target.select('div:nth-of-type(3)')[0].text.strip()
            target_limit = target.select('div:nth-of-type(4)')[0].text.strip()
            list.append(target_num)
            list.append(target_title)
            list.append(target_date)
            list.append(target_limit)
            list.append(target_url)
            full_list.append(list)


    except:
        Error = '에러가 발생했습니다! URL을 확인해주세요.\nURL : ' + kocca_url + '\n'
        return Error

    result = []
    result.append('##### 콘텐츠진흥원 지원사업 #####' + '\n')
    text_list = ['사업번호', '제목', '등록일', '접수기간', 'URL']

    for idx in range(len(full_list)):
        target = full_list[idx]
        result.append('INDEX = ' + str(idx))
        for i in range(5):
            result.append(text_list[i] + ' : ' + target[i])
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

kocca()