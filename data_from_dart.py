import requests
import json
from pandas.io.json import json_normalize

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
print('총', len(result), '건')
print(result.head())

# 설정한 회사의 최근 공시 URL
df = result[:10] #10을 고치는 것으로 갯수 조절 가능
for ix, row in df.iterrows():
    url_tmpl = 'http://dart.fss.or.kr/dsaf001/main.do?rcpNo={}'
    url = url_tmpl.format(row['rcp_no'])
    print(ix,url)

