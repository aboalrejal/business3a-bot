import telebot
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "✅ البوت شغال يا أحمد! جاهز لصيد العروض 🔥")

print("🤖 البوت بدأ التشغيل...")
bot.polling()
