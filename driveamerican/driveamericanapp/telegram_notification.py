import telebot

TOKEN = "957100995:AAHi9hNCPViSiaLz7b-s2_wivjOlsFtT-Dk"
CHAT_ID = "104299473"

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message):
    # save_chat_info(message.chat.id)
    print(message.chat.id)
    bot.send_message(message.chat.id, "Этот бот служит для уведомления о приходе на сайт DriveAmerican уведомления!")


def send_message(message):
    bot.send_message(chat_id=CHAT_ID, text=message)


if __name__ == "__main__":
    bot.polling()
