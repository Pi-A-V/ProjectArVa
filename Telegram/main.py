import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup
from config import BOT_TOKEN
from requests import post
from io import StringIO

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

reply_keyboard = [['/data', '/interpreter'],
                  ['/reg', '/fav']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


async def start(update, context):
    await update.message.reply_text(
        "Я бот-справочник. Чем вы хотите воспользоваться?",
        reply_markup=markup
    )


async def help(update, context):
    await update.message.reply_text(
        f"Я бот справочник по Python.")


async def data(update, context):
    reply_keyboard = [['pip', 'print', 'class'],
                      ['type', 'range', 'round'],
                      ['input', 'def', 'len']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    await update.message.reply_text(
        "Это справочник базовых комманд Python. Какая информация вам нужна?",
        reply_markup=markup
    )
    return 2


async def interpreter(update, context):
    await update.message.reply_text(
        "Добро пожаловать в Интерпритатор Python!\n"
        "Чтобы выйти, используйте /menu\n"
        "Напишите свой код, и получите его результат:")
    return 1


async def interpreter_response(update, context):
    req_text = update.message.text
    file = StringIO(req_text)
    user_reply = post('http://127.0.0.1:8080/api/interpreter/krindy', files={'key': file}).text
    await update.message.reply_text(user_reply)

async def data_response(update, context):
    global line_numbers
    comm_name = update.message.text
    if comm_name == 'pip':
        line_numbers = [2, 3, 4, 5]
    elif comm_name == 'print':
        line_numbers = [7, 8, 9, 10]
    elif comm_name == 'class':
        line_numbers = [12, 13, 14, 15,
                        16, 17, 18, 19, 20,
                        21, 22, 23, 24, 25,
                        26, 27, 28, 29, 30,
                        31, 32, 33, 34, 35,
                        36, 37, 38, 39, 40]
    elif comm_name == 'type':
        line_numbers = [42, 43, 44]
    elif comm_name == 'range':
        line_numbers = [46, 47, 48, 49, 50,
                        51, 52, 53, 54, 55]
    elif comm_name == 'round':
        line_numbers = [57, 58, 59, 60, 61, 62, 63]
    elif comm_name == 'input':
        line_numbers = [65, 66, 67, 68, 69, 70]
    elif comm_name == 'def':
        line_numbers = [73, 74, 75, 76, 77]
    elif comm_name == 'len':
        line_numbers = [79, 80, 81, 82, 83, 84, 85]
    with open("doc.txt", 'r', encoding='utf-8') as fp:
        # lines to read
        # To store lines
        lines = []
        for i, line in enumerate(fp):
            # read line 4 and 7
            if i in line_numbers:
                lines.append(line.strip())
    un = '\n'.join(lines)
    await update.message.reply_text(un)

async def menu(update, context):
    await update.message.reply_text("Возвращаю вас в меню...")
    return ConversationHandler.END


async def reg(update, context):
    await update.message.reply_text(
        f"Функция Регистрация в разработке")


async def fav(update, context):
    await update.message.reply_text(
        f"Функция Избранное в разработке")


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    conv_handler = ConversationHandler(
        # Точка входа в диалог.
        # В данном случае — команда /start. Она задаёт первый вопрос.
        entry_points=[CommandHandler('interpreter', interpreter), CommandHandler('data', data)],

        # Состояние внутри диалога.
        # Вариант с двумя обработчиками, фильтрующими текстовые сообщения.
        states={
            # Функция читает ответ на первый вопрос и задаёт второй.
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, interpreter_response)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, data_response)]},

        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[CommandHandler('menu', menu)]
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("data", data))
    application.add_handler(CommandHandler("interpreter", interpreter))
    application.add_handler(CommandHandler("reg", reg))
    application.add_handler(CommandHandler("fav", fav))
    application.add_handler(CommandHandler("help", help))
    application.run_polling()


if __name__ == '__main__':
    main()
