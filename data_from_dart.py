import requests
import json
from pandas.io.json import json_normalize
import pandas as pd
import os
import re
from datetime import datetime
import sqlite3

auth = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
headers={'Referer':'https://dart.fss.or.kr/dsap001/guide.do'}

pdf_link_tmpl = "http://dart.fss.or.kr/pdf/download/pdf.do?rcp_no={rcp_no}&dcm_no={dcm_no}"
excel_link_tmpl = "http://dart.fss.or.kr/pdf/download/excel.do?rcp_no={rcp_no}&dcm_no={dcm_no}&lang=ko"
ifrs_link_tmpl = "http://dart.fss.or.kr/pdf/download/ifrs.do?rcp_no={rcp_no}&dcm_no={dcm_no}&lang=ko"

conn = sqlite3.connect('dart.db')

#오늘(혹은 전일) 공시 100건
def today_announce():
    recent_tmpl = 'http://dart.fss.or.kr/api/search.json?auth={auth}&page_set=100'
    recent= recent_tmpl.format(auth=auth)
    rc = requests.get(recent, headers = headers)
    today_json = json.loads(rc.text)
    today_result = json_normalize(today_json, 'list')
    #print(today_result)


#특정 회사 공시

company_tmpl = 'http://dart.fss.or.kr/api/search.json?auth={auth}&crp_cd={code}&start_dt=19990101&bsn_tp=A001&bsn_tp=A002&bsn_tp=A003&page_set=100'
company = company_tmpl.format(auth=auth, code='005930')
r = requests.get(company, headers=headers)
c_json = json.loads(r.text)
result = json_normalize(c_json, 'list')
#print('총', len(result), '건')
#print(result.head())


# 설정한 회사의 최근 공시 URL

df = result[:10] #10을 고치는 것으로 갯수 조절 가능
for ix, row in df.iterrows():
    url_tmpl = 'http://dart.fss.or.kr/dsaf001/main.do?rcpNo={}'
    url = url_tmpl.format(row['rcp_no'])
    #print(ix,url)

#설정한 회사의 rcp_no 받아오기
def get_rcp_no(code):
    company_tmpl = 'http://dart.fss.or.kr/api/search.json?auth={auth}&crp_cd={code}&start_dt=19990101&bsn_tp=A001&bsn_tp=A002&bsn_tp=A003&page_set=100'
    company = company_tmpl.format(auth=auth, code=code)
    r = requests.get(company, headers=headers)
    c_json = json.loads(r.text)
    result = json_normalize(c_json, 'list')
    df = result[:10] #10개 받아오기. 갯수는 조절 가능
    rcp_no_list = []
    for ix, row in df.iterrows():
        rcp_no_list.append(row['rcp_no'])
    return rcp_no_list

#접수번호(rcp_no)에 해당하는 모든 하위문서 URL 추출
def get_report_doc_urls(rcp_no):
    doc_urls = []
    url = 'http://dart.fss.or.kr/dsaf001/main.do?rcpNo=%s'%(rcp_no)
    r = requests.get(url)
    reg = re.compile('viewDoc\((.*)\);')
    params = []
    matches = reg.findall(r.text)
    for m in matches:
        params.append(m.replace("'", "").replace(" ", "").split(","))

    doc_url_tmpl = "http://dart.fss.or.kr/report/viewer.do?rcpNo=%s&dcmNo=%s&eleId=%s&offset=%s&length=%s&dtd=%s"

    for p in params:
        if rcp_no == p[0]:
            doc_urls.append(doc_url_tmpl % tuple(p))

    return doc_urls

#첨부파일 url 가져오기
def get_report_attach_urls(rcp_no):
    attach_urls = []

    url = "http://dart.fss.or.kr/dsaf001/main.do?rcpNo=%s" % (rcp_no)
    r = requests.get(url)

    start_str = "javascript: viewDoc\('" + rcp_no + "', '"
    end_str = "', null, null, null,"
    reg = re.compile(start_str + '(.*)' + end_str)
    m = reg.findall(r.text)
    dcm_no = m[0]

    attach_urls.append(pdf_link_tmpl.format(rcp_no=rcp_no, dcm_no=dcm_no))
    attach_urls.append(excel_link_tmpl.format(rcp_no=rcp_no, dcm_no=dcm_no))
    attach_urls.append(ifrs_link_tmpl.format(rcp_no=rcp_no, dcm_no=dcm_no))
    return attach_urls

rcp_no = '20170515003806'
attach_urls = get_report_attach_urls(rcp_no)


#pdf문서 저장하기
def save_pdf():
    url = attach_urls[0]
    fname = '005930_' + rcp_no + '.pdf'

    with open(fname, 'wb') as f:
        f.write(requests.get(url).content)

#엑셀문서 저장하기
def save_excel():
    url = attach_urls[1]
    fname = '005930_' + rcp_no + '.xls'

    with open(fname, 'wb') as f:
        f.write(requests.get(url).content)

#ZIP 문서 저장하기
def save_zip():
    url = attach_urls[2]
    fname = '005930_' + rcp_no + '.zip'

    with open(fname, 'wb') as f:
        f.write(requests.get(url).content)

#save_pdf()
#save_excel()
#save_zip()

#finance_state = pd.read_excel('005930_20170515003806.xls', sheet_name = '연결 재무상태표', index_col=0, skiprows=6)
#interest = pd.read_excel('005930_20170515003806.xls', sheet_name = '연결 손익계산서', index_col=0, skiprows=6)
#cash_flow = pd.read_excel('005930_20170515003806.xls', sheet_name = '현금흐름표', index_col=0, skiprows=7)


#url을 파일로 저장
def wget(url, to=None):
    local_filename = url.split('/')[-1]
    if to:
        local_filename = to
    r = requests.get(url, stream = True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size = 1024):
            if chunk:
                f.write(chunk)
                f.flush()
    if os.path.getsize(local_filename) <= 0:
        os.remove(local_filename)
        return None
    return local_filename

xls_url = 'http://dart.fss.or.kr/pdf/download/excel.do?rcp_no=20170515003806&dcm_no=5653406&lang=ko'

#지정한 종목 코드의 보고서 가져오기(기간)
def get_dart_report(code, start_dt = None, end_dt = None):
    url_tmpl = 'http://dart.fss.or.kr/api/search.json?'\
               'page_set=100&auth={auth}&crp_cd={code}&start_dt={start_dt}&end_dt={end_dt}&page_no={page_no}'
    url = url_tmpl.format(auth=auth, code=code, start_dt=start_dt, end_dt=end_dt, page_no=1)

    if start_dt == None:
        start_dt = datetime.today().strftime('%Y%m%d')
    if end_dt == None:
        end_dt = datetime.today().strftime('%Y%m%d')

    r = requests.get(url, headers = headers)
    jo = json.loads(r.text)
    df = json_normalize(jo, 'list')

    for page in range(2, jo['total_page'] + 1):
        url = url_tmpl.format(auth=auth, code=code, start_dt=start_dt, end_dt=end_dt, page_no=page)
        r = requests.get(url, headers = headers)
        jo = json.loads(r.text)
        df = df.append(json_normalize(jo, 'list'))

    cols = {'crp_cd' : '종목코드', 'crp_cls' : '법인구분', 'crp_nm' : '종목명', 'flr_nm' : '제출인', 'rcp_dt' : '접수일', 'rcp_no' : '접수번호', 'rmk' : '비고', 'rpt_nm' : '보고서명'}
    df.rename(columns = cols, inplace = True)
    df['접수일'] = pd.to_datetime(df['접수일'])
    df.set_index('접수일', inplace=True)
    return df

#SQL로 DB화하기
def make_db():
    create_sql = """
    CREATE TABLE IF NOT EXISTS "stock_dart" (
      "접수날짜" TIMESTAMP,
      "종목코드" TEXT,
      "법인구분" TEXT,
      "종목명" TEXT,
      "제출인" TEXT,
      "접수번호" TEXT,
      "비고" TEXT,
      "보고서명" TEXT,
      UNIQUE("접수번호") ON CONFLICT REPLACE
    );
    """
    return create_sql


conn.execute(make_db())
conn.execute('CREATE INDEX IF NOT EXISTS "ix_stock_dart_date"ON "stock_dart" ("접수일")')
conn.execute('CREATE INDEX IF NOT EXISTS "ix_stock_Dart_code"ON "stock_dart" ("종목코드")')
