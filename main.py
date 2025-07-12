import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

BOT_TOKEN = "8098899276:AAG11NDceA9arPPjAqMPkoA2xPQzFaIHD5g"

# گرفتن قیمت از بیت‌پین
def get_bitpin_price(symbol="btc"):
    url = "https://api.bitpin.ir/v1/mkt/markets/"
    try:
        res = requests.get(url).json()
        for item in res["results"]:
            if symbol in item["code"]:
                return f"{item['title_fa']} در بیت‌پین: {int(item['price']):,} تومان"
        return "ارز مورد نظر در بیت‌پین پیدا نشد."
    except:
        return "خطا در دریافت قیمت از بیت‌پین."

# گرفتن قیمت از بای‌بیت
def get_bybit_price(symbol="BTCUSDT"):
    url = f"https://api.bybit.com/v2/public/tickers?symbol={symbol.upper()}"
    try:
        res = requests.get(url).json()
        price = float(res["result"][0]["last_price"])
        return f"{symbol.upper()} در بای‌بیت: {price:,.2f} دلار"
    except:
        return "خطا در دریافت قیمت از بای‌بیت."

# مدیریت پیام‌ها
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    
    if "بیت‌کوین" in text or "btc" in text:
        msg = get_bitpin_price("btc") + "\n" + get_bybit_price("BTCUSDT")
    elif "اتریوم" in text or "eth" in text:
        msg = get_bitpin_price("eth") + "\n" + get_bybit_price("ETHUSDT")
    elif "تتر" in text or "usdt" in text:
        msg = get_bitpin_price("usdt") + "\n" + get_bybit_price("USDTUSDT")
    else:
        msg = "برای دریافت قیمت بزن: بیت‌کوین | اتریوم | تتر"

    await update.message.reply_text(msg)

# اجرای ربات
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
