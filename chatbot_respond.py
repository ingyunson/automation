import telegram
from stock_crawler_for_bot import stockinfo
from datetime import datetime
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


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


def get_command(bot, update):
    print("get")
    button_list = build_button(["on", "off", "cancel"])  # make button list
    show_markup = InlineKeyboardMarkup(build_menu(button_list, len(button_list) - 1))  # make markup
    update.message.reply_text("원하는 값을 선택하세요", reply_markup=show_markup)  # reply text with markup


def callback_get(bot, update):
    data_selected = update.callback_query.data
    print("callback : ", data_selected)
    if data_selected.find("cancel") != -1:
        bot.edit_message_text(text="취소하였습니다.",
                              chat_id=update.callback_query.message.chat_id,
                              message_id=update.callback_query.message.message_id)
        return

    if len(data_selected.split(",")) == 1:
        button_list = build_button(["1", "2", "3", "cancel"], data_selected)
        show_markup = InlineKeyboardMarkup(build_menu(button_list, len(button_list) - 1))
        bot.edit_message_text(text="상태를 선택해 주세요.",
                              chat_id=update.callback_query.message.chat_id,
                              message_id=update.callback_query.message.message_id,
                              reply_markup=show_markup)

    elif len(data_selected.split(",")) == 2:
        bot.edit_message_text(text="{}이(가) 선택되었습니다".format(update.callback_query.data),
                              chat_id=update.callback_query.message.chat_id,
                              message_id=update.callback_query.message.message_id)


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
    updater = Updater("492877807:AAEcHwvVyI8Sc9Bj31izc_cBanq0v4BZq24")
    my_token = '492877807:AAEcHwvVyI8Sc9Bj31izc_cBanq0v4BZq24'
    chatbot = telegram.Bot(token=my_token)
    chat_id = '68008527'

    now = datetime.now()

    dp = updater.dispatcher

    #    message_handler = MessageHandler(Filters.text, get_message)  # 텍스트에 반응하여 get_message 함수를 호출
    #    updater.dispatcher.add_handler(message_handler)  # updater에 message_handler를 더해줌

    help_handler = CommandHandler('help', help_command)  # help 명령에 반응하여 help_command 함수를 호출
    updater.dispatcher.add_handler(help_handler)

    get_handler = CommandHandler('get', get_command)
    updater.dispatcher.add_handler(get_handler)
    updater.dispatcher.add_handler(CallbackQueryHandler(callback_get))

    # stock_handler = CommandHandler('stock', stock_command)
    # updater.dispatcher.add_handler(stock_handler)

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

