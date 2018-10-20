from IPython.display import HTML, display
import re
import requests
import json
import pandas as pd
from pandas.io.json import json_normalize


display(HTML('<iframe width="500" height="600" src="https://goo.gl/TUiGst"></iframe>'))


def naver_finstate_detail(cmp_cd, rpt='0', frq='1', finGubun='IFRSL'):
    '''
    네이버 파이낸스로 부터 상세재무제표를 읽어온다
    * cmp_cd:  # 종목코드: '005930'
    * rpt='0' # 종류: '0'=손익계산서(기본값), '1'=재무상태표, '2'=현금흐름표
    * frq='1' # 기간: '0'=연간, '1'=분기(기본값)
    * finGubun='IFRSL' # 구분: 'MAIN'=주재무제표, 'IFRSS'=KIFRS별도, 'IFRSL'=IFRS연결(기본값), 'GAAPS'=GAAP개별, 'GAAPL'=GAAP연결
    '''

    # encparam 가져오기
    url = 'http://companyinfo.stock.naver.com/v1/company/c1030001.aspx?cmp_cd=005930'
    html_text = requests.get(url).text
    encparam = re.findall("encparam: '(.*?)'", html_text)[0]

    url_tmpl = 'http://companyinfo.stock.naver.com/v1/company/cF3002.aspx?' \
               'cmp_cd={cmp_cd}&frq={frq}&rpt={rpt}&finGubun={finGubun}&frqTyp={frq}&cn=&encparam={encparam}'

    url = url_tmpl.format(cmp_cd=cmp_cd, frq=frq, rpt=rpt, finGubun=finGubun, frqTyp=frq, encparam=encparam)

    # 페이지 가져오기
    headers = {'Referer': url}
    jo = json.loads(requests.get(url, headers=headers).text)

    # DataFrame 생성
    df = json_normalize(jo, 'DATA')

    # DATA1~DATA6 컬럼 이름 바꾸기
    jo_yymm = jo['YYMM'][:6]
    date_str_list = []
    for yymm in jo_yymm:
        m = re.search('(\d{4}/\d{0,2}).*', yymm)
        date_str_list.append(m.group(1) if m else '')
    data_n_list = ['DATA' + str(i) for i in range(1, 7)]
    yymm_cols = zip(data_n_list, date_str_list)
    cols_map = dict(yymm_cols)
    df.rename(columns=cols_map, inplace=True)
    df['ACC_NM'] = df['ACC_NM'].str.strip().replace('[\.*\[\]]', '', regex=True)
    df.set_index(['ACCODE', 'ACC_NM'], inplace=True)
    df = df.iloc[:, 1:7]  # 날짜 컬럼만 추출
    df = df.T  # Transpose (컬럼, 인덱스 바꾸기)
    df.index = pd.to_datetime(df.index)
    df.index.name = '날짜'
    return df