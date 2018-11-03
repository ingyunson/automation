import pandas as pd
import urllib.request
from bs4 import BeautifulSoup
import openpyxl

code_df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13', header=0)[0]

# 종목코드가 6자리이기 때문에 6자리를 맞춰주기 위해 설정해줌
code_df.종목코드 = code_df.종목코드.map('{:06d}'.format)

# 우리가 필요한 것은 회사명과 종목코드이기 때문에 필요없는 column들은 제외해준다.
code_df = code_df[['회사명', '종목코드']]

# 한글로된 컬럼명을 영어로 바꿔준다.
code_df = code_df.rename(columns={'회사명': 'name', '종목코드': 'code'})
code_df.head()


# 종목 이름을 입력하면 종목에 해당하는 코드를 불러와
# 네이버 금융(http://finance.naver.com)에 넣어줌

def open_file(stock_code):
    filename = get_file(stock_code)
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

    print("요청 URL = {}".format(url))
    return url

def get_url_2(item_name, code_df):
    code = code_df.query("name=='{}'".format(item_name))['code'].to_string(index=False)
    url = 'https://companyinfo.stock.naver.com/v1/company/c1010001.aspx?cmp_cd={code}&cn='.format(code=code)

    print("요청 URL2 = {}".format(url))
    return url

target_stock = []


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
            # item_list = ['주식코드', 'EPS', 'BPS', 'PER', '업종PER', 'PBR', '현금배당수익률']
            # print(item_list[index] + ' : ' + b.get_text())
            # info.append(item_list[index] + ' : ' + b.get_text())
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


for name in code_df.name:
    stockdata(name)
    print(target_stock)

stock_code = []
except_code = []
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

print(stock_name)
