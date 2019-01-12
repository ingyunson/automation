import requests
import datetime
import json
import telegram

#공공 오픈 API를 이용하여 외환 정보 받아오기
def api_set(day):
    date = day.strftime('%Y-%m-%d')
    api_key = <API KEY>
    api = 'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={key}&searchdate={date}&data={data}'.format(
        key=api_key, date=date, data='AP01')
    req = requests.get(api)
    get_data = req.text
    currency_json = json.loads(get_data)

    return currency_json


def main():
    today = datetime.date.today() #오늘 날짜를 datetime형으로 가져오기
    yesterday = today - datetime.timedelta(1) #오늘 정보가 없을 경우 어제 정보를 가져오기 위해 어제 날짜를 datetime형으로 가져오기

    result = ['***오늘 {day}의 환율입니다.***\n주말 혹은 당일 정보 업데이트가 되지 않으면 전일(주말의 경우 금요일)의 정보가 표시됩니다.\n'.format(day=today)] #최종 표시될 메시지
    cur_list = {'AED': 0, 'AUD': 1, 'BHD': 2, 'CAD': 3, 'CHF': 4, 'CNH': 5, 'DKK': 6, 'EUR': 7, 'GBP': 8, 'HKD': 9,
                'IDR': 10, 'JPY': 11, 'KRW': 12, 'KWD': 13, 'MYR': 14, 'NOK': 15, 'NZD': 16, 'SAR': 17, 'SEK': 18,
                'SGD': 19, 'THB': 20, 'USD': 21} #제공하는 외환 리스트

    currency = ('USD', 'CNH', 'JPY', 'EUR') #읽어들일 외환 리스트



    if not api_set(today): #오늘 날짜를 입력했을 때 API가 빈 정보를 반환할 경우 어제 날짜를 입력하여 정보 가져옴
        raw = api_set(yesterday)
    else: # API 반환 정보가 비어있지 않을 경우 당일 날짜를 입력하여 정보 가져옴
        raw = api_set(today)

    for curr in currency: #currency 변수로 설정해 둔 외환 리스트 정보 가공
        num = cur_list[curr]
        data = (raw[num]['cur_nm'], raw[num]['cur_unit'], raw[num]['deal_bas_r'])
        draft = '현재 {cur_name}({cur_unit})의 기준환율은 {currency}원입니다.'.format(cur_name=data[0], cur_unit=data[1], currency=data[2])
        result.append(draft)

    text = "\n".join(result) #챗봇으로 보내기 좋게 메시지 가공



    my_token = <TELEGRAM TOKEN>  # botfather로 받은 토큰
    chatbot = telegram.Bot(token=my_token)
    chat_id = <CHATID OR CHANNEL ADDRESS>  # 채널의 경우 @채널주소
    chatbot.sendMessage(chat_id=chat_id, text=text) #최종 결과물인 text 변수를 챗봇으로 발송


if __name__ == '__main__':
    main()