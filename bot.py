import os
import random
from datetime import datetime
from telegram.ext import Application, CommandHandler, MessageHandler, filters

TELEGRAM_TOKEN = os.environ["9068837266:AAGuKsWvoEFkbaqblqgjBMko_r8abgJ1bgc"]

notes = []
expenses = []
todos = []

quotes = [
    "Делай сегодня то, за что завтра скажешь себе спасибо.",
    "Маленькие шаги каждый день дают большой результат.",
    "Не жди идеального момента — начинай сейчас.",
    "Ты справишься. Просто начни с одного действия.",
    "Дисциплина важнее мотивации."
]

async def start(update, context):
    await update.message.reply_text(
        "Привет! Я твой личный бот.\n\n"
        "Напиши /help, чтобы увидеть все команды."
    )

async def help_command(update, context):
    await update.message.reply_text(
        "Команды:\n\n"
        "/заметка текст — сохранить заметку\n"
        "/заметки — все заметки\n"
        "/удалить_заметку номер — удалить заметку\n\n"
        "/дело текст — добавить дело\n"
        "/дела — список дел\n"
        "/сделано номер — отметить дело выполненным\n\n"
        "/расход 500 — записать расход\n"
        "/итог — сумма расходов\n\n"
        "/время — текущее время\n"
        "/мотивация — случайная мотивация\n"
        "/кубик — бросить кубик\n"
        "/монетка — орёл или решка\n"
        "/анекдот — короткая шутка"
    )

async def add_note(update, context):
    if not context.args:
        await update.message.reply_text("Пример: /заметка купить хлеб")
        return
    note = " ".join(context.args)
    notes.append(note)
    await update.message.reply_text(f"Заметка сохранена: {note}")

async def show_notes(update, context):
    if not notes:
        await update.message.reply_text("Заметок пока нет.")
        return
    text = "\n".join(f"{i + 1}. {n}" for i, n in enumerate(notes))
    await update.message.reply_text("Заметки:\n" + text)

async def delete_note(update, context):
    try:
        number = int(context.args[0]) - 1
        removed = notes.pop(number)
        await update.message.reply_text(f"Удалено: {removed}")
    except (IndexError, ValueError):
        await update.message.reply_text("Пример: /удалить_заметку 1")

async def add_todo(update, context):
    if not context.args:
        await update.message.reply_text("Пример: /дело сделать уроки")
        return
    todo = " ".join(context.args)
    todos.append({"text": todo, "done": False})
    await update.message.reply_text(f"Дело добавлено: {todo}")

async def show_todos(update, context):
    if not todos:
        await update.message.reply_text("Дел пока нет.")
        return
    lines = []
    for i, todo in enumerate(todos):
        status = "✅" if todo["done"] else "⬜"
        lines.append(f"{i + 1}. {status} {todo['text']}")
    await update.message.reply_text("Дела:\n" + "\n".join(lines))

async def complete_todo(update, context):
    try:
        number = int(context.args[0]) - 1
        todos[number]["done"] = True
        await update.message.reply_text(f"Выполнено: {todos[number]['text']}")
    except (IndexError, ValueError):
        await update.message.reply_text("Пример: /сделано 1")

async def add_expense(update, context):
    try:
        amount = float(context.args[0].replace(",", "."))
        expenses.append(amount)
        await update.message.reply_text(f"Расход записан: {amount}")
    except (IndexError, ValueError):
        await update.message.reply_text("Пример: /расход 500")

async def show_total(update, context):
    await update.message.reply_text(f"Всего расходов: {sum(expenses)}")

async def time_now(update, context):
    now = datetime.now().strftime("%d.%m.%Y %H:%M")
    await update.message.reply_text(f"Сейчас: {now}")

async def motivation(update, context):
    await update.message.reply_text(random.choice(quotes))

async def dice(update, context):
    await update.message.reply_text(f"Выпало: {random.randint(1, 6)}")

async def coin(update, context):
    await update.message.reply_text(random.choice(["Орёл", "Решка"]))

async def joke(update, context):
    jokes = [
        "Почему программисты любят тёмную тему? Потому что свет притягивает баги.",
        "Я хотел рассказать шутку про UDP, но не уверен, дошло ли она.",
        "Кофе — это способ превратить понедельник в JavaScript."
    ]
    await update.message.reply_text(random.choice(jokes))

async def auto_reply(update, context):
    text = update.message.text.lower()

    answers = {
        "привет": "Привет! Чем помочь?",
        "как дела": "Работаю нормально! А у тебя как?",
        "что умеешь": "Напиши /help — покажу все команды.",
        "спасибо": "Всегда пожалуйста!",
        "пока": "Пока! Возвращайся.",
        "кто ты": "Я твой личный Telegram-бот.",
        "помоги": "Напиши /help — там все команды."
    }

    for phrase, answer in answers.items():
        if phrase in text:
            await update.message.reply_text(answer)
            return

    await update.message.reply_text("Я пока понимаю только команды. Напиши /help.")

app = Application.builder().token(TELEGRAM_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("заметка", add_note))
app.add_handler(CommandHandler("заметки", show_notes))
app.add_handler(CommandHandler("удалить_заметку", delete_note))
app.add_handler(CommandHandler("дело", add_todo))
app.add_handler(CommandHandler("дела", show_todos))
app.add_handler(CommandHandler("сделано", complete_todo))
app.add_handler(CommandHandler("расход", add_expense))
app.add_handler(CommandHandler("итог", show_total))
app.add_handler(CommandHandler("время", time_now))
app.add_handler(CommandHandler("мотивация", motivation))
app.add_handler(CommandHandler("кубик", dice))
app.add_handler(CommandHandler("монетка", coin))
app.add_handler(CommandHandler("анекдот", joke))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply))

print("Бот запущен")
app.run_polling()
