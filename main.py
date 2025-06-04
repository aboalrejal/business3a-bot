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
        current_price_el = product.select_one(".promo-price")
        old_price_el = product.select_one(".promo-price--old")

        if not current_price_el or not old_price_el:
            return "❌ Bol.com: لا يوجد خصم كافي حالياً"

        price_now = float(current_price_el.text.strip().replace("€", "").replace(",", "."))
        price_before = float(old_price_el.text.strip().replace("€", "").replace(",", "."))
        discount = round(((price_before - price_now) / price_before) * 100)

        if discount < 50:
            return "❌ Bol.com: الخصم أقل من 50% - تم تجاهله"

        return (
            f"📌 من Bol.com\n"
            f"📦 {title}\n"
            f"💰 السعر الحالي: €{price_now}\n"
            f"❌ السعر السابق: €{price_before}\n"
            f"📉 الخصم: {discount}%\n"
            f"🔗 {link}"
        )
    except Exception as e:
        return f"❌ Bol.com: خطأ - {str(e)}"

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
        current_price_el = product.select_one(".price")
        old_price_el = product.select_one(".old-price")

        if not current_price_el or not old_price_el:
            return "❌ Gamma: لا يوجد خصم كافي حالياً"

        price_now = float(current_price_el.text.strip().replace("€", "").replace(",", "."))
        price_before = float(old_price_el.text.strip().replace("€", "").replace(",", "."))
        discount = round(((price_before - price_now) / price_before) * 100)

        if discount < 50:
            return "❌ Gamma: الخصم أقل من 50% - تم تجاهله"

        return (
            f"📌 من Gamma\n"
            f"📦 {title}\n"
            f"💰 السعر الحالي: €{price_now}\n"
            f"❌ السعر السابق: €{price_before}\n"
            f"📉 الخصم: {discount}%\n"
            f"🔗 {link}"
        )
    except Exception as e:
        return f"❌ Gamma: خطأ - {str(e)}"

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
        current_price_el = product.select_one(".sales-price")
        old_price_el = product.select_one(".list-price")

        if not current_price_el or not old_price_el:
            return "❌ Blokker: لا يوجد خصم كافي حالياً"

        price_now = float(current_price_el.text.strip().replace("€", "").replace(",", "."))
        price_before = float(old_price_el.text.strip().replace("€", "").replace(",", "."))
        discount = round(((price_before - price_now) / price_before) * 100)

        if discount < 50:
            return "❌ Blokker: الخصم أقل من 50% - تم تجاهله"

        return (
            f"📌 من Blokker\n"
            f"📦 {title}\n"
            f"💰 السعر الحالي: €{price_now}\n"
            f"❌ السعر السابق: €{price_before}\n"
            f"📉 الخصم: {discount}%\n"
            f"🔗 {link}"
        )
    except Exception as e:
        return f"❌ Blokker: خطأ - {str(e)}"

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
        price_el = product.select_one(".a-price .a-offscreen")
        old_price_el = product.select_one(".a-text-price .a-offscreen")

        if not (title_el and link_el and price_el and old_price_el):
            return "❌ Amazon: لا يوجد خصم كافي حالياً"

        title = title_el.text.strip()
        link = "https://www.amazon.nl" + link_el["href"]
        price_now = float(price_el.text.replace("€", "").replace(",", ".").strip())
        price_before = float(old_price_el.text.replace("€", "").replace(",", ".").strip())
        discount = round(((price_before - price_now) / price_before) * 100)

        if discount < 50:
            return "❌ Amazon: الخصم أقل من 50% - تم تجاهله"

        return (
            f"📌 من Amazon\n"
            f"📦 {title}\n"
            f"💰 السعر الحالي: €{price_now}\n"
            f"❌ السعر السابق: €{price_before}\n"
            f"📉 الخصم: {discount}%\n"
            f"🔗 {link}"
        )
    except Exception as e:
        return f"❌ Amazon: خطأ - {str(e)}"

@bot.message_handler(commands=['deals'])
def send_all_deals(message):
    deals = [
        get_from_bol(),
        get_from_gamma(),
        get_from_blokker(),
        get_from_amazon()
    ]
    results = [deal for deal in deals if not deal.startswith("❌ الخصم أقل")]
    bot.send_message(message.chat.id, "\n\n".join(results) if results else "❌ لا يوجد عروض بخصم 50٪ أو أكثر حالياً.")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "👋 أهلاً بك في بوت العروض!\nأرسل /deals لجلب المنتجات المخفضة بنسبة 50٪ أو أكثر 🔥")

bot.remove_webhook()
print("🤖 البوت التجاري يعمل...")
bot.polling()
