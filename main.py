import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler
from telegram import ReplyKeyboardMarkup
from config import BOT_TOKEN

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

reply_keyboard = [['/data', '/interpreter'],
                  ['/reg', '/fav']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


async def help(update, context):
    await update.message.reply_text(
        "Я бот справочник по Python.")


async def data(update, context):
    await update.message.reply_text(
        "Адрес: г. Москва, ул. Льва Толстого, 16")


async def interpreter(update, context):
    await update.message.reply_text("Функция Интерпритатор в разработке")


async def reg(update, context):
    await update.message.reply_text(
        "Функция Регистрация в разработке")


async def fav(update, context):
    await update.message.reply_text(
        "Функция Избранное в разработке")


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("data", data))
    application.add_handler(CommandHandler("interpreter", interpreter))
    application.add_handler(CommandHandler("reg", reg))
    application.add_handler(CommandHandler("fav", fav))
    application.add_handler(CommandHandler("help", help))
    application.run_polling()


if __name__ == '__main__':
    main()
