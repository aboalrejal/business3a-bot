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

# 🟢 1. Pepper
def get_from_pepper():
    url = "https://www.pepper.nl"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    first = soup.select_one("article.thread")
    if not first:
        return "❌ Pepper: لا يوجد عرض حالياً"
    
    title = first.select_one(".thread-title").text.strip()
    link = url + first.select_one("a.thread-title")["href"]
    price = first.select_one(".thread-price").text.strip() if first.select_one(".thread-price") else "❓"

    return f"📌 من Pepper\n📦 {title}\n💰 {price}\n🔗 {link}"

# 🟢 2. Bol
def get_from_bol():
    url = "https://www.bol.com/nl/nl/l/aanbiedingen/47915/"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    product = soup.select_one("li.product-item--row")
    if not product:
        return "❌ Bol: لا يوجد عرض حالياً"
    
    title = product.select_one("a.product-title").text.strip()
    link = "https://www.bol.com" + product.select_one("a.product-title")["href"]
    price = product.select_one(".promo-price").text.strip() if product.select_one(".promo-price") else "❓"

    return f"📌 من Bol.com\n📦 {title}\n💰 {price}\n🔗 {link}"

# 🟢 3. Gamma
def get_from_gamma():
    url = "https://www.gamma.nl/aanbiedingen"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    product = soup.select_one(".product-tile")
    if not product:
        return "❌ Gamma: لا يوجد عرض حالياً"
    
    title = product.select_one(".title").text.strip()
    link = "https://www.gamma.nl" + product.select_one("a")["href"]
    price = product.select_one(".price").text.strip() if product.select_one(".price") else "❓"

    return f"📌 من Gamma\n📦 {title}\n💰 {price}\n🔗 {link}"

# 📦 أمر واحد يجلب من الثلاثة
@bot.message_handler(commands=['deals'])
def send_all_deals(message):
    deals = [
        get_from_pepper(),
        get_from_bol(),
        get_from_gamma()
    ]
    response = "\n\n".join(deals)
    bot.send_message(message.chat.id, response)

# 📩 اختبار
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "أهلاً بك في بوت العروض! 🛒\nأرسل /deals للحصول على أحدث المنتجات الرخيصة 🔥")

print("🤖 البوت التجاري يعمل...")
bot.polling()
