import os
import telebot
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

USER_CHAT_ID = 556136331

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

def get_from_amazon():
    try:
        url = "https://www.amazon.nl/s?k=aanbiedingen"
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        product = soup.select_one(".s-result-item")
        if not product:
            return None
        title = product.select_one("h2 a span").text.strip()
        link = "https://www.amazon.nl" + product.select_one("h2 a")["href"]
        now = product.select_one(".a-price .a-offscreen").text
        before = product.select_one(".a-text-price .a-offscreen").text
        price_now, price_before, discount = extract_prices(now, before)
        if discount and discount >= 50:
            return f"📌 من Amazon\n📦 {title}\n💰 الآن: €{price_now}\n❌ قبل: €{price_before}\n📉 خصم: {discount}%\n🔗 {link}"
    except:
        return None

def get_from_coolblue():
    try:
        url = "https://www.coolblue.nl/aanbiedingen"
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        product = soup.select_one(".product-card")
        if not product:
            return None
        title = product.select_one(".product-card__title").text.strip()
        link = "https://www.coolblue.nl" + product.select_one("a")["href"]
        now = product.select_one(".sales-price__current").text
        before = product.select_one(".sales-price__former").text
        price_now, price_before, discount = extract_prices(now, before)
        if discount and discount >= 50:
            return f"📌 من Coolblue\n📦 {title}\n💰 الآن: €{price_now}\n❌ قبل: €{price_before}\n📉 خصم: {discount}%\n🔗 {link}"
    except:
        return None

def get_from_ikea():
    try:
        url = "https://www.ikea.com/nl/nl/offers/"
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        product = soup.select_one(".pip-product-compact")
        if not product:
            return None
        title = product.select_one(".pip-header-section__title--small").text.strip()
        link = "https://www.ikea.com" + product.select_one("a")["href"]
        now = product.select_one(".pip-price__value").text
        before = product.select_one(".pip-price__previous").text
        price_now, price_before, discount = extract_prices(now, before)
        if discount and discount >= 50:
            return f"📌 من IKEA\n📦 {title}\n💰 الآن: €{price_now}\n❌ قبل: €{price_before}\n📉 خصم: {discount}%\n🔗 {link}"
    except:
        return None

def get_from_mediamarkt():
    try:
        url = "https://www.mediamarkt.nl/nl/category/_aanbiedingen-700281.html"
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        product = soup.select_one(".product-wrapper")
        if not product:
            return None
        title = product.select_one(".product-title").text.strip()
        link = "https://www.mediamarkt.nl" + product.select_one("a")["href"]
        now = product.select_one(".price").text
        before = product.select_one(".price-was").text
        price_now, price_before, discount = extract_prices(now, before)
        if discount and discount >= 50:
            return f"📌 من Mediamarkt\n📦 {title}\n💰 الآن: €{price_now}\n❌ قبل: €{price_before}\n📉 خصم: {discount}%\n🔗 {link}"
    except:
        return None

def collect_deals():
    return list(filter(None, [
        get_from_bol(),
        get_from_gamma(),
        get_from_blokker(),
        get_from_amazon(),
        get_from_coolblue(),
        get_from_ikea(),
        get_from_mediamarkt()
    ]))

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, "👋 أهلاً بك في بوت العروض
اكتب /deals لجلب أفضل العروض 🔥")

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

print("🤖 البوت يعمل تلقائيًا + يدويًا...")
bot.polling()
