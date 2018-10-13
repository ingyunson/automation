import requests
import json
from pandas.io.json import json_normalize
import re

auth = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
headers={'Referer':'https://dart.fss.or.kr/dsap001/guide.do'}

#오늘(혹은 전일) 공시 100건
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

doc_urls = get_report_doc_urls(get_rcp_no('005930')[0])
print(len(doc_urls))
for url in doc_urls:
    print(url)