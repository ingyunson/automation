# coding=utf8

import telegram
from stock_crawler_for_bot import stockinfo
from currency_crawler_for_bot import currency_get
from datetime import datetime
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
new = []

# chat_id = chatbot.getUpdates()[-1].message.chat.id

def get_message(bot, update):
    update.message.reply_text('현재 사용 가능한 명령어는 다음과 같습니다.\n'
                              '/stock : 주식 정보 검색')


def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


def build_button(text_list, callback_header=""):  # make button list
    button_list = []
    text_header = callback_header
    if callback_header != "":
        text_header += ","

    for text in text_list:
        button_list.append(InlineKeyboardButton(text, callback_data=text_header + text))

    return button_list


# 환율 검색 모듈


def currency_command(bot, update):
    update.message.reply_text('환율 검색 엔진입니다. 환율 정보를 받아오는 중이니 잠시만 기다려주세요.')
    currency_target = ['미국 USD', '유럽연합 EUR', '일본 JPY (100엔)', '중국 CNY', '홍콩 HKD', '대만 TWD']
    now = datetime.now()
    message = ['***오늘 ' + str('%s-%s-%s' % (now.year, now.month, now.day )) + '의 주요 통화 환율은 다음과 같습니다.***']
    money_data = currency_get()
    for key in money_data:
        if key in currency_target:
            value = money_data.get(key)
            message.append(key + '의 환율은 ' + str(value) + '원입니다.')
        else:
            pass
    text = "\n".join(message)
    update.message.reply_text(text)
    currency_list = ["미국 USD", "유럽연합 EUR", "일본 JPY (100엔)", '중국 CNY', '홍콩 HKD', '대만 TWD', '호주 AUD', '영국 GBP', '캐나다 CAD', '스위스 CHF', '스웨덴 SEK', '뉴질랜드 NZD', '체코 CZK', '칠레 CLP', '터키 TRY', '이스라엘 ILS', '덴마크 DKK', '노르웨이 NOK', '사우디아라비아 SAR', '쿠웨이트 KWD', '아랍에미리트 AED', '요르단 JOD', '이집트 EGP', '태국 THB', '싱가포르 SGD', '말레이시아 MYR', '인도네시아 IDR 100', '카타르 QAR', '카자흐스탄 KZT',  '인도 INR', '파키스탄 PKR', '방글라데시 BDT', '필리핀 PHP', '멕시코 MXN', '브라질 BRL', '베트남 VND 100', '남아프리카 공화국 ZAR', '러시아 RUB', '헝가리 HUF', '폴란드 PLN']
    temp_list = []
    idx = 0
    for i in range(len(currency_list)):
        header = ""
        if header != "":
            header += ","
        if idx < 4:
            temp_list.append(InlineKeyboardButton(currency_list[i], callback_data=header + currency_list[i]))
            idx = idx + 1
        else :
            idx = 0
            new.append(temp_list)
            temp_list = []
            temp_list.append(InlineKeyboardButton(currency_list[i], callback_data=header + currency_list[i]))
            idx = idx + 1
    show_markup = InlineKeyboardMarkup(new)  # make markup
    update.message.reply_text("원하는 값을 선택하세요", reply_markup=show_markup)  # reply text with markup


def callback_get(bot, update):
    data_selected = update.callback_query.data
    get_data = currency_get()
    print("callback : ", data_selected)
    if data_selected.find("cancel") != -1:
        bot.edit_message_text(text="취소하였습니다.",
                              chat_id=update.callback_query.message.chat_id,
                              message_id=update.callback_query.message.message_id)
        return

    if len(data_selected.split(",")) == 1:
        data = get_data.get(data_selected)
        show_markup = InlineKeyboardMarkup(new)
        #button_list = build_button(["미국 USD", "유럽연합 EUR", "일본 JPY (100엔)", "cancel"])
        #show_markup = InlineKeyboardMarkup(build_menu(button_list, len(button_list) - 1))
        bot.edit_message_text(text='검색하신 ' + data_selected + '의 환율은 ' + data + '원입니다.',
                              chat_id=update.callback_query.message.chat_id,
                              message_id=update.callback_query.message.message_id,
                              reply_markup=show_markup)
        print(data)


# 주식 검색 모듈

def stock(bot, update):
    #    user = update.message.from_user
    update.message.reply_text(
        '안녕하세요! 주식 검색 봇입니다!'
        '/cancel 을 입력하시면 사용을 중단합니다.\n\n'
        '검색을 원하시는 주식의 이름을 입력해주세요')

    return STOCK


def stock_search(bot, update):
    update.message.reply_text('검색하신 주식의 정보는 다음과 같습니다.')
    user = update.message.from_user
    answer = update.message.text
    print('searching')
    data = stockinfo(answer)
    text = "\n".join(data)
    update.message.reply_text(text)
    update.message.reply_text('다른 알고 싶은 주식의 이름을 입력해주세요. 중단을 원하시면 /cancel 을 입력해주세요.')
    return STOCK


def cancel(bot, update):
    # user = update.message.from_user
    logger.info("User canceled the conversation.")
    update.message.reply_text('이용해주셔서 감사합니다.\n'
                              '다시 주식 정보를 검색하고 싶으시면 /stock 명령을 이용해 주세요.')

    return ConversationHandler.END


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


STOCK = range(0)


def main():
    updater = Updater(<TOKEN>)
    my_token = <TOKEN>
    chatbot = telegram.Bot(token=my_token)
    chat_id = <YOUR_ID>

    now = datetime.now()

    dp = updater.dispatcher

    currency_handler = CommandHandler('currency', currency_command)
    updater.dispatcher.add_handler(currency_handler)
    updater.dispatcher.add_handler(CallbackQueryHandler(callback_get))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('stock', stock)],

        states={
            STOCK: [MessageHandler(Filters.text, stock_search)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)
    dp.add_error_handler(error)

    chatbot.sendMessage(chat_id=chat_id, text='텔레그램봇이 준비되었습니다. /stock으로 주식 검색을 시작하세요')
    print('Bot is ready.')
    updater.start_polling()  # polling 시작
    updater.idle()  # updater가 종료되지 않고 계속 실행되고 있도록


if __name__ == '__main__':
    main()