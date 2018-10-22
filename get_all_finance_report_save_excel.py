from get_finance_report_excel import naver_finstate_detail
import itertools
import FinanceDataReader as fdr
import pandas as pd


frq_list = [('0', '연간'), ('1', '분기') ]
rpt_list = [('0', '손익계산서'), ('1', '재무상태표'), ('2', '현금흐름표')]

krx_list = fdr.StockListing('KRX')

for ix, row in krx_list[:10].iterrows():  # 10종목만 시행
    fn = "%s_%s_재무제표.xlsx" % (row['Symbol'], row['Name'])
    print(fn)
    writer = pd.ExcelWriter(fn)
    for frq, rpt in itertools.product(frq_list,  rpt_list):
        df = naver_finstate_detail(row['Symbol'], rpt=rpt[0], frq=frq[0])
        df.to_excel(writer, sheet_name=rpt[1] + '_' + frq[1])
    writer.save()