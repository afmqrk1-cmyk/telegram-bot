import os
import google.generativeai as genai
from telegram.ext import Application, CommandHandler, MessageHandler, filters

TELEGRAM_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
GEMINI_KEY = os.environ["GEMINI_API_KEY"]

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

async def start(update, context):
    await update.message.reply_text("Привет! Напиши любой вопрос — я отвечу.")

async def help_command(update, context):
    await update.message.reply_text("Просто напиши мне сообщение, и я отвечу через ИИ.")

async def ai_chat(update, context):
    question = update.message.text
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    try:
        response = model.generate_content(question)
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text("Ошибка ИИ: " + str(e))

app = Application.builder().token(TELEGRAM_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_chat))

print("Бот запущен")
app.run_polling()
