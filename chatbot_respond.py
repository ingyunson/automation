import telegram
from datetime import datetime
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

my_token = '492877807:AAEcHwvVyI8Sc9Bj31izc_cBanq0v4BZq24'
chatbot = telegram.Bot(token=my_token)
chat_id = '68008527'
# chat_id = chatbot.getUpdates()[-1].message.chat.id
updater = Updater(my_token)

now = datetime.now()

print('starting telegram bot')
chatbot.sendMessage(chat_id=chat_id, text='Telegrambot is Ready')


def get_message(bot, update):
    update.message.reply_text('got Text')  # 'got text'를 답장
    update.message.reply_text(update.message.text)  # 받은 메시지를 답장


def help_command(bot, update):
    update.message.reply_text("무엇을 도와드릴까요?")


def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu

def build_button(text_list, callback_header = "") : # make button list
    button_list = []
    text_header = callback_header
    if callback_header != "" :
        text_header += ","

    for text in text_list :
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
    if data_selected.find("cancel") != -1 :
        bot.edit_message_text(text="취소하였습니다.",
                              chat_id=update.callback_query.message.chat_id,
                              message_id=update.callback_query.message.message_id)
        return

    if len(data_selected.split(",")) == 1 :
        button_list = build_button(["1", "2", "3", "cancel"], data_selected)
        show_markup = InlineKeyboardMarkup(build_menu(button_list, len(button_list) - 1))
        bot.edit_message_text(text="상태를 선택해 주세요.",
                              chat_id=update.callback_query.message.chat_id,
                              message_id=update.callback_query.message.message_id,
                              reply_markup=show_markup)

    elif len(data_selected.split(",")) == 2 :
        bot.edit_message_text(text="{}이(가) 선택되었습니다".format(update.callback_query.data),
                              chat_id=update.callback_query.message.chat_id,
                              message_id=update.callback_query.message.message_id)


updater = Updater(my_token)  # my_token에 업데이트된 사항이있으면 가져옴

message_handler = MessageHandler(Filters.text, get_message)  # 텍스트에 반응하여 get_message 함수를 호출
updater.dispatcher.add_handler(message_handler)  # updater에 message_handler를 더해줌

help_handler = CommandHandler('help', help_command)  # help 명령에 반응하여 help_command 함수를 호출
updater.dispatcher.add_handler(help_handler)

get_handler = CommandHandler('get', get_command)
updater.dispatcher.add_handler(get_handler)
updater.dispatcher.add_handler(CallbackQueryHandler(callback_get))

updater.start_polling(timeout=3, clean=True)  # polling 시작
updater.idle()  # updater가 종료되지 않고 계속 실행되고 있도록