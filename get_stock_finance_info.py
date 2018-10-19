import re
from datetime import datetime
import pandas as pd
import requests
from bs4 import BeautifulSoup
from io import StringIO

'''
get_date_str(s) - 문자열 s 에서 "YYYY/MM" 문자열 추출
'''


def get_date_str(s):
    date_str = ''
    r = re.search("\d{4}/\d{2}", s)
    if r:
        date_str = r.group()
        date_str = date_str.replace('/', '-')

    return date_str


'''
* code: 종목코드
* fin_type = '0': 재무제표 종류 (0: 주재무제표, 1: GAAP개별, 2: GAAP연결, 3: IFRS별도, 4:IFRS연결)
* freq_type = 'Y': 기간 (Y:년, Q:분기)
'''


def get_finstate_naver(code, fin_type='0', freq_type='Y'):
    # encparam, encid  추출
    url_tmpl = 'http://companyinfo.stock.naver.com/v1/company/c1010001.aspx?cmp_cd=%s'
    url = url_tmpl % (code)

    html_text = requests.get(url).text
    encparam = re.findall("encparam: '(.*?)'", html_text)[0]
    encid = re.findall("id: '(.*?)'", html_text)[0]

    #  재무데이터 표 추출
    url_tmpl = 'http://companyinfo.stock.naver.com/v1/company/ajax/cF1001.aspx?' \
               'cmp_cd=%s&fin_typ=%s&freq_typ=%s&encparam=%s&id=%s'

    url = url_tmpl % (code, fin_type, freq_type, encparam, encid)

    header = {
        'Referer': 'https://companyinfo.stock.naver.com/v1/company/c1010001.aspx',
    }

    html_text = requests.get(url, headers=header).text
    dfs = pd.read_html(StringIO(html_text))
    df = dfs[1]
    if df.iloc[0, 0].find('해당 데이터가 존재하지 않습니다') >= 0:
        return None

    cols = list(df.columns)
    new_cols = []
    new_cols.append(cols[0][0])
    new_cols += [c[1] for c in cols[:-1]]
    df.columns = new_cols
    df.rename(columns={'주요재무정보': 'date'}, inplace=True)
    df.set_index('date', inplace=True)
    df.columns = [get_date_str(x) for x in df.columns]

    dft = df.T
    dft.index = pd.to_datetime(dft.index)

    # remove if index is NaT
    dft = dft[pd.notnull(dft.index)]
    return dft


