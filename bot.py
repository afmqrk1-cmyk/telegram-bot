from telegram.ext import Application, CommandHandler

TOKEN = "9068837266:AAF8JpYXmUCE_2LGSxaSwUJmFFW7SZstpvM"

async def start(update, context):
    await update.message.reply_text("Привет! Бот работает.")

async def help_command(update, context):
    await update.message.reply_text("Команды:\n/start — проверить\n/help — помощь")

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))

print("Бот запущен")
app.run_polling()
