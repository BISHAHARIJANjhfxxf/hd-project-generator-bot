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

users = {}

keyboard = ReplyKeyboardMarkup(
    [
        ["➕ Add Text"],
        ["📊 Table Mode"],
        ["🔤 Font Size"],
        ["🎨 Heading Color"],
        ["📄 Generate"],
        ["🗑 Reset"]
    ],
    resize_keyboard=True
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users[update.effective_user.id] = {
        "text": "",
        "font": 15,
        "color": "black"
    }
    await update.message.reply_text("Bot Ready ✅", reply_markup=keyboard)

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    msg = update.message.text

    if user_id not in users:
        await update.message.reply_text("Type /start first")
        return

    data = users[user_id]

    if msg == "🗑 Reset":
        data["text"] = ""
        await update.message.reply_text("Cleared")
        return

    if msg == "🔤 Font Size":
        context.user_data["font"] = True
        await update.message.reply_text("Send number like 12 or 15")
        return

    if context.user_data.get("font"):
        data["font"] = int(msg)
        context.user_data["font"] = False
        await update.message.reply_text("Font updated")
        return

    if msg == "🎨 Heading Color":
        context.user_data["color"] = True
        await update.message.reply_text("Send color name or hex")
        return

    if context.user_data.get("color"):
        data["color"] = msg
        context.user_data["color"] = False
        await update.message.reply_text("Color updated")
        return

    if msg == "📊 Table Mode":
        context.user_data["table"] = True
        data["text"] += "#table\n"
        await update.message.reply_text("Send rows using | and type DONE")
        return

    if context.user_data.get("table"):
        if msg == "DONE":
            data["text"] += "#endtable\n"
            context.user_data["table"] = False
            await update.message.reply_text("Table added")
        else:
            data["text"] += msg + "\n"
        return

    if msg == "📄 Generate":
        file = generate_pdf(data["text"], data["font"], data["color"])
        await update.message.reply_document(document=open(file, "rb"))
        return

    # Default text add
    data["text"] += msg + "\n"
    await update.message.reply_text("Added")

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

app.run_polling()
