import os
import telebot
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

headers = {
    "User-Agent": "Mozilla/5.0"
}

# Bol.com
def get_from_bol():
    try:
        url = "https://www.bol.com/nl/nl/l/aanbiedingen/47915/"
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        product = soup.select_one("li.product-item--row")
        if not product:
            return "❌ Bol.com: لا يوجد عرض حالياً"

        title = product.select_one("a.product-title").text.strip()
        link = "https://www.bol.com" + product.select_one("a.product-title")["href"]
        price = product.select_one(".promo-price").text.strip() if product.select_one(".promo-price") else "❓"

        return f"📌 من Bol.com\n📦 {title}\n💰 {price}\n🔗 {link}"
    except Exception as e:
        return f"❌ Bol.com: خطأ - {str(e)}"

# Gamma
def get_from_gamma():
    try:
        url = "https://www.gamma.nl/aanbiedingen"
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        product = soup.select_one(".product-tile")
        if not product:
            return "❌ Gamma: لا يوجد عرض حالياً"

        title = product.select_one(".title").text.strip()
        link = "https://www.gamma.nl" + product.select_one("a")["href"]
        price = product.select_one(".price").text.strip() if product.select_one(".price") else "❓"

        return f"📌 من Gamma\n📦 {title}\n💰 {price}\n🔗 {link}"
    except Exception as e:
        return f"❌ Gamma: خطأ - {str(e)}"

# Blokker
def get_from_blokker():
    try:
        url = "https://www.blokker.nl/aanbiedingen"
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        product = soup.select_one(".product-grid .product-item")
        if not product:
            return "❌ Blokker: لا يوجد عرض حالياً"

        title = product.select_one(".product-title").text.strip()
        link = "https://www.blokker.nl" + product.select_one("a")["href"]
        price = product.select_one(".sales-price").text.strip() if product.select_one(".sales-price") else "❓"

        return f"📌 من Blokker\n📦 {title}\n💰 {price}\n🔗 {link}"
    except Exception as e:
        return f"❌ Blokker: خطأ - {str(e)}"

# Amazon
def get_from_amazon():
    try:
        url = "https://www.amazon.nl/s?k=aanbiedingen"
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        product = soup.select_one(".s-result-item")
        if not product:
            return "❌ Amazon: لا يوجد عرض حالياً"

        title_el = product.select_one("h2 a span")
        link_el = product.select_one("h2 a")
        price_el = product.select_one(".a-price span")

        if not (title_el and link_el and price_el):
            return "❌ Amazon: مشكلة في قراءة البيانات"

        title = title_el.text.strip()
        link = "https://www.amazon.nl" + link_el["href"]
        price = price_el.text.strip()

        return f"📌 من Amazon\n📦 {title}\n💰 {price}\n🔗 {link}"
    except Exception as e:
        return f"❌ Amazon: خطأ - {str(e)}"

# أمر /deals
@bot.message_handler(commands=['deals'])
def send_all_deals(message):
    deals = [
        get_from_bol(),
        get_from_gamma(),
        get_from_blokker(),
        get_from_amazon()
    ]
    bot.send_message(message.chat.id, "\n\n".join(deals))

# أمر /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "👋 أهلاً بك في بوت العروض!\nأرسل /deals لجلب المنتجات الرخيصة من المتاجر الهولندية 🔥")

print("🤖 البوت التجاري يعمل...")
bot.polling()
