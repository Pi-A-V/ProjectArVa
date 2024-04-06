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
        "Я бот-справочник. Какая информация вам нужна?",
        reply_markup=markup
    )


async def help(update, context):
    await update.message.reply_text(
        f"Я бот справочник по Python.")


async def data(update, context):
    await update.message.reply_text(
        f"Функция в разработке")


async def interpreter(update, context):
    await update.message.reply_text(
        "Добро пожаловать в Интерпритатор Python!\n"
        "Чтобы выйти, используйте /stop\n"
        "Напишите свой код, и получите его результат:")
    return 1


async def first_response(update, context):
    req_text = update.message.text
    file = StringIO(req_text)
    user_reply = post('http://127.0.0.1:8080/api/interpreter/krindy', files={'key': file}).text
    await update.message.reply_text(user_reply)


async def stop(update, context):
    await update.message.reply_text("Всего доброго!")
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
        entry_points=[CommandHandler('interpreter', interpreter)],

        # Состояние внутри диалога.
        # Вариант с двумя обработчиками, фильтрующими текстовые сообщения.
        states={
            # Функция читает ответ на первый вопрос и задаёт второй.
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, first_response)]},

        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[CommandHandler('stop', stop)]
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
