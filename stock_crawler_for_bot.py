import pandas as pd
import urllib.request
from bs4 import BeautifulSoup

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


# 'class'속성값이 'num'인 'b' 태그를 모두 찾는다.
def stockinfo(item_name):
    #print('조회를 원하는 주식의 이름을 넣어주세요')
    info = []
    url1 = get_url_1(item_name, code_df)
    url2 = get_url_2(item_name, code_df)
    f = urllib.request.urlopen(url2).read()
    soup = BeautifulSoup(f, 'html.parser')
    print('\n오늘의 ' + str(item_name) + '의 기업정보 \n')
    bs = soup.find_all('b', {'class': 'num'})
    for index, b in enumerate(bs):
        item_list = ['주식코드', 'EPS', 'BPS', 'PER', '업종PER', 'PBR', '현금배당수익률']
        #print(item_list[index] + ' : ' + b.get_text())
        info.append(item_list[index] + ' : ' + b.get_text())
    return info