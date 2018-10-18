#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests
import pandas as pd
from datetime import datetime, timedelta
from dateutil import parser
from pandas.io.json import json_normalize
import sqlite3

# 지정한 날짜의 보고서 전체 가져오기
'''
get_dart_report_day
* date(str): 'yyyymmdd' (지정하지 않으면 오늘)
'''


def get_dart_report_day(date=None):
    auth = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    headers = {'Referer': 'https://dart.fss.or.kr/dsap001/guide.do'}

    if date == None:
        date = datetime.today().strftime('%Y%m%d')

    url_tmpl = 'http://dart.fss.or.kr/api/search.json?' \
               'page_set=100&auth={auth}&start_dt={start_dt}&end_dt={end_dt}&page_no={page_no}'
    url = url_tmpl.format(auth=auth, start_dt=date, end_dt=date, page_no=1)
    r = requests.get(url, headers=headers)
    jo = json.loads(r.text)
    df = json_normalize(jo, 'list')

    for page in range(2, jo['total_page'] + 1):
        url = url_tmpl.format(auth=auth, start_dt=date, end_dt=date, page_no=page)
        r = requests.get(url, headers=headers)
        jo = json.loads(r.text)
        df = df.append(json_normalize(jo, 'list'))

    cols = {'crp_cd': '종목코드', 'crp_cls': '법인구분', 'crp_nm': '종목명', 'flr_nm': '제출인',
            'rcp_dt': '접수날짜', 'rcp_no': '접수번호', 'rmk': '비고', 'rpt_nm': '보고서명'}
    df.rename(columns=cols, inplace=True)
    if len(df) == 0:
        return df
    df['접수날짜'] = pd.to_datetime(df['접수날짜'])
    df.set_index('접수날짜', inplace=True)
    return df


if __name__ == "__main__":
    conn = sqlite3.connect('dart.db')

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
    conn.execute(create_sql)
    conn.execute('CREATE INDEX IF NOT EXISTS "ix_stock_dart_detail_date"ON "stock_dart" ("접수날짜")')
    conn.execute('CREATE INDEX IF NOT EXISTS "ix_stock_dart_detail_code"ON "stock_dart" ("종목코드")')

    # 기본 시작일: 1999년 4월 1일, DART 서비스 시작
    start_dt = datetime(1999, 4, 1)
    start_dt = datetime(2018, 8, 1)  # 테스트를 위한 코드 (삭제하면 1999년 부터 시작)

    # 마지막 접수날짜를 읽어 기본 시작일로 지정
    df_tmp = pd.read_sql('select max(접수날짜) from stock_dart', conn)
    if df_tmp.iloc[0, 0]:
        start_dt = parser.parse(df_tmp.iloc[0, 0])
        print(start_dt)

    # 오늘까지
    end_dt = datetime.today()
    end_dt = datetime(2018, 8, 30)  # 테스트를 위한 코드 (삭제하면 오늘까지)

    # 시작일(start_dt) ~ 종료일(end_dt) 까지
    dt = end_dt - start_dt
    for i in range(dt.days + 1):
        the_day = start_dt + timedelta(days=i)
        df = get_dart_report_day(the_day.strftime('%Y%m%d'))
        df.to_sql('stock_dart', conn, if_exists='append')
        print(the_day.strftime('%Y%m%d'), len(df), 'rows')