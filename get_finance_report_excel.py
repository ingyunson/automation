import re
import requests
import json
import pandas as pd
from pandas.io.json import json_normalize


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

# 재무상태표 (BS), 재무항목 코드
df_code_bs = pd.read_csv('https://goo.gl/iQ9QJ1', dtype={'재무코드':str})
df_code_bs.set_index('재무코드', inplace=True)

# 포괄손익계산서 (IS), 재무항목 코드
df_code_is = pd.read_csv('https://goo.gl/EtGyUT', dtype={'재무코드':str})
df_code_is.set_index('재무코드', inplace=True)

# 현금흐름표 (CF), 재무항목 코드
df_code_cf = pd.read_csv('https://goo.gl/6tTX6A', dtype={'재무코드':str})
df_code_cf.set_index('재무코드', inplace=True)

# 201370 영업이익 # 202210 금융수익 # 202550 금융비용 # 204410 기타영업외손익 # 203120 법인세비용차감전계속사업이익
is_cols = ['201370', '202210', '202550', '204410', '203120']

# 110000 자산총계 # 110010 비유동자산 # 110610 무형자산 # 130000 부채총계 # 131580 유동부채
bs_cols = ['110000', '110010', '110610', '130000', '131580']

# 400010 당기순이익 # 400810 이자수익 # 402360 단기금융자산의감소 # 403880 이익잉여금의증가 # 404580 무형자산의증가
cf_cols = ['400010', '400810', '402360', '403880', '404580']

# 삼성전자, 손익계산서(IS), 연간, IFRS연결
df_is = naver_finstate_detail(cmp_cd='005930', rpt='0', frq='0')
df_is = df_is[is_cols]

# 삼성전자, 재무상태표(BS), 연간, IFRS연결
df_bs = naver_finstate_detail(cmp_cd='005930', rpt='1', frq='0')
df_bs = df_bs[bs_cols]

# 삼성전자, 현금흐름표(CF), 연간, IFRS연결
df_cf = naver_finstate_detail(cmp_cd='005930', rpt='2', frq='0')
df_cf = df_cf[cf_cols]

writer = pd.ExcelWriter('삼성전자 주요 재무항목.xlsx')
df_is.to_excel(writer, sheet_name='손익계산서_연간')
df_bs.to_excel(writer, sheet_name='재무상태표_연간')
df_cf.to_excel(writer, sheet_name='현금흐름표_연간')
writer.save()