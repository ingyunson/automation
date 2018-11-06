# -*- coding: utf-8 -*-

import os
import pandas as pd
import urllib.request
from bs4 import BeautifulSoup
import openpyxl
import telegram

#target_stock = []
target_stock = ['세이브존I&C', '지역난방공사', '코리아써키트', '한창제지', '에스코넥', '에이티세미콘', '원익테라세미콘', '주성엔지니어링', 'BGF', '한국금융지주', '한일홀딩스', '한전KPS', '현대해상', '화승인더스트리', 'APS홀딩스', '국순당', '베셀', '성우하이텍', '예림당', '참좋은여행', '코위버', '크리스에프앤씨', 'SK텔레콤', '금양', '농심홀딩스', '일진디스플', '티웨이홀딩스', '풍산홀딩스', '한국공항', '바텍', '서플러스글로벌', '시공테크', '에스에프에이', '유니셈', '유티아이', '인탑스', '토비스', '피제이메탈', 'DB하이텍', 'JW홀딩스', '남선알미늄', '디와이파워', '삼성전자', '코오롱글로벌', '한국전자홀딩스', '한전산업', '한화생명', 'SKC 솔믹스', '동진쎄미켐', '메카로', '세원물산', '제이씨현시스템', 'KPX홀딩스', 'SK이노베이션', '대성산업', '현대제철', '나이스정보통신', '다우데이타', '모다이노칩', '에버다임', '이스트아시아홀딩스', '정다운', '파라텍', '한솔시큐어', '메리츠화재', '아주캐피탈', '에이피티씨', '디와이', '새론오토모티브', '쌍용양회공업', '케이씨텍', '현대글로비스', 'HB테크놀러지', 'KNN', '슈피겐코리아', '이엘피', '제이엠티', '파워넷', '한국알콜', 'DRB동일', '동일산업', '미래에셋대우', '미원상사', '에스제이엠', '효성', '매커스', '시스웍', '아이앤씨', '오션브릿지', '이베스트투자증권', '제룡산업']
stock_code = []
except_code = []


#### 텔레그램 봇 설정
my_token = '729504243:AAFQEqyGx_yjOkSEBoNCUToP2KLH0VR-WX4' #botfather로 받은 토큰
chatbot = telegram.Bot(token = my_token)
#chat_id = '@krx_stock' #채널의 경우 @채널주소
chat_id = chatbot.getUpdates()[-1].message.chat.id




#### 주식 데이터 가져오기
code_df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13', header=0)[0]

# 종목코드가 6자리이기 때문에 6자리를 맞춰주기 위해 설정해줌
code_df.종목코드 = code_df.종목코드.map('{:06d}'.format)

# 우리가 필요한 것은 회사명과 종목코드이기 때문에 필요없는 column들은 제외해준다.
code_df = code_df[['회사명', '종목코드']]

# 한글로된 컬럼명을 영어로 바꿔준다.
code_df = code_df.rename(columns={'회사명': 'name', '종목코드': 'code'})


# 종목 이름을 입력하면 종목에 해당하는 코드를 불러와
# 네이버 금융(http://finance.naver.com)에 넣어줌

def search(dirname):
    filenames = os.listdir(dirname)
    filelist = []
    for filename in filenames:
        ext = os.path.splitext(filename)[-1]
        if ext == '.xlsx':
            filelist.append(filename)
    return filelist


def get_file(stock_code):
    file_list = search(r"c:\Users\Seimei\Jupyter") # 경로 수정 필요
    for s in file_list:
        if stock_code in s:
            return s


def open_file(stock_code):
    filename = r'c:\Users\Seimei\Jupyter\\' + get_file(stock_code) # 경로 수정 필요
    book = openpyxl.load_workbook(filename)
    sheet1 = book.worksheets[0]
    sheet2 = book.worksheets[1]
    data = []
    for row in sheet1.rows:
        data.append([row[0].value, row[59].value])  # 0:년도, 1:영업이익, 2:부채총계, 3:자본총계

    for i, row in enumerate(sheet2.rows):
        data[i][2:] = [row[109].value, row[188].value]  # 0:년도, 1:영업이익, 2:부채총계, 3:자본총계
    del data[0:3]

    for i in range(len(data)):
        if data[i][0]:
            years = data[i][0].year
            data[i][0] = years
        else:
            pass
    return data


def get_url_1(item_name, code_df):
    code = code_df.query("name=='{}'".format(item_name))['code'].to_string(index=False)
    url = 'http://finance.naver.com/item/sise_day.nhn?code={code}'.format(code=code)
    return url


def get_url_2(item_name, code_df):
    code = code_df.query("name=='{}'".format(item_name))['code'].to_string(index=False)
    url = 'https://companyinfo.stock.naver.com/v1/company/c1010001.aspx?cmp_cd={code}&cn='.format(code=code)
    return url


def stockdata(item_name):
    try:
        info = []
        url1 = get_url_1(item_name, code_df)
        url2 = get_url_2(item_name, code_df)
        f = urllib.request.urlopen(url2).read()
        soup = BeautifulSoup(f, 'html.parser')
        print('\n오늘의 ' + str(item_name) + '의 기업정보 \n')
        bs = soup.find_all('b', {'class': 'num'})
        stock_info = []
        for index, b in enumerate(bs):
            stock_info.append(b.get_text())
        price = soup.select('#cTB11 > tbody > tr:nth-of-type(1) > td > strong')[0].get_text().strip()
        code = stock_info[0]
        EPS = stock_info[1]
        BRS = stock_info[2]
        PER = stock_info[3]
        area_PER = stock_info[4]
        PBR = stock_info[5]
        dive = stock_info[6]

        if float(PER) < 10 and float(PBR) < 5 and price > BRS and price < EPS * 10:
            target_stock.append(item_name)
            print(item_name)
        else:
            print('Not available')
    except:
        print('it has error!')

    return target_stock


def return_stock():
    # for name in code_df.name:
    #    stockdata(name)

    stock_name = []

    for i in target_stock:
        code = code_df.query("name=='{}'".format(i))['code'].to_string(index=False)
        stock_code.append(code)

    for num in stock_code:
        try:
            info = open_file(num)
            if info[-1][1] > 0 and info[-2][1] > 0 and (info[-1][2] / info[-1][3]) < 3 and (
                    info[-1][3] - info[-2][3]) > 0:  # 영업이익이 양수, 부채비율이 300% 미만, 2년 연속 흑자
                print(info[-1])
                except_code.append(num)
            else:
                print(info[-2])
                if info[-2][1] > 0 and info[-3][1] > 0 and (info[-2][2] / info[-2][3]) < 3 and (
                        info[-2][3] - info[-3][3]) > 0:
                    except_code.append(num)
                else:
                    print('no data')
        except:
            print('error!')

    for code in except_code:
        name = code_df.query("code=='{}'".format(code))['name'].to_string(index=False)
        stock_name.append(name)
    return stock_name

message_list = []

def bot_message():
    name = return_stock()
    chatbot.sendMessage(chat_id=chat_id, text='오늘의 조건에 맞는 주식은 다음과 같습니다.\n ※조건 : PER이 10 미만, PBR이 5 미만, 가격이 EPS의 10배 미만, 2년간 영업이익이 흑자, 부채비율 300% 미만\n\n')
    for i in name:
        info = []
        url1 = get_url_1(i, code_df)
        url2 = get_url_2(i, code_df)
        f = urllib.request.urlopen(url2).read()
        soup = BeautifulSoup(f, 'html.parser')
        bs = soup.find_all('b', {'class': 'num'})
        stock_info = []
        for index, b in enumerate(bs):
            stock_info.append(b.get_text())
        price = soup.select('#cTB11 > tbody > tr:nth-of-type(1) > td > strong')[0].get_text().strip()
        code = stock_info[0]
        EPS = stock_info[1]
        BRS = stock_info[2]
        PER = stock_info[3]
        area_PER = stock_info[4]
        PBR = stock_info[5]
        dive = stock_info[6]

        message_list.append('{i}\n기업정보 링크 {url2}'.format(i = i, url2 = url2))

    t = '\n\n'.join(message_list)
    chatbot.send_message(chat_id = chat_id, text = t)

        #message_list.append('{i}의 정보는 다음과 같습니다.\n주식번호 : {code}\n전일 주가 : {price}원\nEPS : {eps}\nBRS : {brs}\nPER : {per}\n업종 PER : {area_per}\nPBR : {pbr}\n현금배당률 : {dive}\n일별 시세 링크 : {url1}\n기업정보 링크 {url2}'.format(i = i, code = code, price = price, eps = EPS, brs = BRS, per = PER, area_per = area_PER, pbr = PBR, dive = dive, url1 = url1, url2 = url2))

    #for t in message_list:
    #    chatbot.sendMessage(chat_id=chat_id, text= t)

    return message_list

print(bot_message())