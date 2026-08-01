import re

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from gstinapi import GstinApi
from config import BOT_TOKEN, GST_API_KEY

api = GstinApi(api_key=GST_API_KEY)

GST_PATTERN = re.compile(
    r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z][1-9A-Z]Z[0-9A-Z]$"
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 GST Verification Bot\n\nGST Number bhejiye."
    )


async def lookup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    gst = update.message.text.strip().upper()

    if not GST_PATTERN.match(gst):
        await update.message.reply_text("❌ Invalid GST Number")
        return

    try:
        result = api.lookup(gst)

        if not result["success"]:
            await update.message.reply_text(result["error"])
            return

        data = result["data"]

        msg = f"""
✅ GST VERIFIED

GSTIN: {data["gstin"]}
Legal Name: {data["legal_name"]}
Trade Name: {data["trade_name"]}
Status: {data["status"]}
Taxpayer Type: {data["taxpayer_type"]}
Registration Date: {data["registration_date"]}
Address: {data["address"]}
Pincode: {data["pincode"]}
State Code: {data["state_code"]}
Block Status: {data["block_status"]}
"""

        await update.message.reply_text(msg)

    except Exception as e:
        await update.message.reply_text(str(e))


app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, lookup))

print("Bot Started...")

app.run_polling()