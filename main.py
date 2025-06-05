import os
import telebot
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
USER_CHAT_ID = os.getenv("USER_CHAT_ID")  # تأكد من وضع هذا المتغير في .env
bot = telebot.TeleBot(BOT_TOKEN)

headers = {
    "User-Agent": "Mozilla/5.0"
}

def extract_prices(now_text, before_text):
    try:
        price_now = float(now_text.replace("€", "").replace(",", ".").strip())
        price_before = float(before_text.replace("€", "").replace(",", ".").strip())
        discount = round(((price_before - price_now) / price_before) * 100)
        return price_now, price_before, discount
    except:
        return None, None, None

def get_from_bol():
    try:
        url = "https://www.bol.com/nl/nl/l/aanbiedingen/47915/"
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        product = soup.select_one("li.product-item--row")
        if not product:
            return None
        title = product.select_one("a.product-title").text.strip()
        link = "https://www.bol.com" + product.select_one("a.product-title")["href"]
        now = product.select_one(".promo-price").text
        before = product.select_one(".promo-price--old").text
        price_now, price_before, discount = extract_prices(now, before)
        if discount and discount >= 50:
            return f"📌 من Bol.com\n📦 {title}\n💰 الآن: €{price_now}\n❌ قبل: €{price_before}\n📉 خصم: {discount}%\n🔗 {link}"
    except:
        return None

def get_from_gamma():
    try:
        url = "https://www.gamma.nl/aanbiedingen"
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        product = soup.select_one(".product-tile")
        if not product:
            return None
        title = product.select_one(".title").text.strip()
        link = "https://www.gamma.nl" + product.select_one("a")["href"]
        now = product.select_one(".price").text
        before = product.select_one(".old-price").text
        price_now, price_before, discount = extract_prices(now, before)
        if discount and discount >= 50:
            return f"📌 من Gamma\n📦 {title}\n💰 الآن: €{price_now}\n❌ قبل: €{price_before}\n📉 خصم: {discount}%\n🔗 {link}"
    except:
        return None

def get_from_blokker():
    try:
        url = "https://www.blokker.nl/aanbiedingen"
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        product = soup.select_one(".product-grid .product-item")
        if not product:
            return None
        title = product.select_one(".product-title").text.strip()
        link = "https://www.blokker.nl" + product.select_one("a")["href"]
        now = product.select_one(".sales-price").text
        before = product.select_one(".list-price").text
        price_now, price_before, discount = extract_prices(now, before)
        if discount and discount >= 50:
            return f"📌 من Blokker\n📦 {title}\n💰 الآن: €{price_now}\n❌ قبل: €{price_before}\n📉 خصم: {discount}%\n🔗 {link}"
    except:
        return None

def collect_deals():
    return list(filter(None, [
        get_from_bol(),
        get_from_gamma(),
        get_from_blokker()
    ]))

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(
        message.chat.id,
        "👋 أهلاً بك في بوت العروض! أرسل /deals لجلب المنتجات الرخيصة من المتاجر الهولندية 🔥"
    )

@bot.message_handler(commands=['deals'])
def send_manual_deals(message):
    deals = collect_deals()
    if deals:
        bot.send_message(message.chat.id, "\n\n".join(deals))
    else:
        bot.send_message(message.chat.id, "❌ لا يوجد عروض حالياً بخصم 50٪ أو أكثر.")

def send_auto_deals():
    deals = collect_deals()
    if deals:
        bot.send_message(USER_CHAT_ID, "📢 عروض جديدة كل يومين:\n\n" + "\n\n".join(deals))
    else:
        bot.send_message(USER_CHAT_ID, "📢 لا يوجد عروض بخصم 50٪ أو أكثر اليوم.")

# ⏱ جدولة تلقائية كل يومين
scheduler = BackgroundScheduler()
scheduler.add_job(send_auto_deals, 'interval', days=2)
scheduler.start()

print("✅ البوت شغّال الآن ومستعد لاستقبال الأوامر.")

bot.infinity_polling()
