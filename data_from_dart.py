import requests
import json

auth = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
headers={'Referer':'https://dart.fss.or.kr/dsap001/guide.do'}

#오늘(혹은 전일) 공시
recent_tmpl = 'http://dart.fss.or.kr/api/search.json?auth={auth}'
recent= recent_tmpl.format(auth=auth)

rc = requests.get(recent, headers = headers)
#print(rc.text)


#특정 회사 공시
company_tmps = 'http://dart.fss.or.kr/api/company.json?auth={auth}&crp_cd={code}'
company = company_tmps.format(auth = auth, code = '005930')
c = requests.get(company, headers = headers)
c_json = json.loads(c.text)
print(c_json)

