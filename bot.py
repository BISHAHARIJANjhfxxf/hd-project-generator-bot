import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
from formatter import generate_pdf

BOT_TOKEN = os.environ.get("BOT_TOKEN")

user_data_store = {}

keyboard = ReplyKeyboardMarkup(
    [
        ["➕ Add Text"],
        ["🔤 Select Font Size"],
        ["🎨 Select Heading Color"],
        ["📄 Generate Project"],
        ["🗑 Reset"]
    ],
    resize_keyboard=True
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data_store[update.effective_user.id] = {
        "text": "",
        "font_size": 15,
        "color": "black"
    }
    await update.message.reply_text("Project Generator Started", reply_markup=keyboard)

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if user_id not in user_data_store:
        return

    if text == "🗑 Reset":
        user_data_store[user_id]["text"] = ""
        await update.message.reply_text("Data Cleared")
        return

    if text == "🔤 Select Font Size":
        await update.message.reply_text("Send font size number (e.g., 12, 15, 18)")
        context.user_data["awaiting_font"] = True
        return

    if text == "🎨 Select Heading Color":
        await update.message.reply_text("Send color name (blue/red/black) or hex (#1F4E79)")
        context.user_data["awaiting_color"] = True
        return

    if text == "📄 Generate Project":
        file_path = generate_pdf(
            user_data_store[user_id]["text"],
            user_data_store[user_id]["font_size"],
            user_data_store[user_id]["color"]
        )
        await update.message.reply_document(document=open(file_path, "rb"))
        return

    if context.user_data.get("awaiting_font"):
        user_data_store[user_id]["font_size"] = int(text)
        context.user_data["awaiting_font"] = False
        await update.message.reply_text("Font size updated")
        return

    if context.user_data.get("awaiting_color"):
        user_data_store[user_id]["color"] = text
        context.user_data["awaiting_color"] = False
        await update.message.reply_text("Heading color updated")
        return

    # Default: add text
    user_data_store[user_id]["text"] += text + "\n"
    await update.message.reply_text("Text added")

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

app.run_polling()
