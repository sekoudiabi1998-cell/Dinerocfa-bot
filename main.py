import os
import random
import threading
from datetime import datetime, timedelta
from flask import Flask, send_from_directory
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

# --- CONFIG DINERO ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
PROMO_CODE = "DINERO06"
LIEN_1WIN = "https://1win.ci/betting?p=unoe&sharebet=DINERO06"
ADMIN_ID = 6312211592
WEBAPP_URL = "https://dinerocfa-bot.onrender.com"  # Ton lien Render

verified_users = set()

# --- SERVEUR WEB POUR MINI APP ---
app_flask = Flask(__name__)

@app_flask.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app_flask.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host="0.0.0.0", port=port)

# --- BOT TELEGRAM ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        f"👋 Bienvenue sur **DINERO CFA PREDICTOR** 🔥\n\n"
        f"Code officiel : **{PROMO_CODE}**\n\n"
        f"1️⃣ Inscris-toi avec {PROMO_CODE}\n"
        f"2️⃣ Envoie ton ID 1WIN\n"
        f"3️⃣ Débloque la Mini App 🚀"
    )
    keyboard = [
        [InlineKeyboardButton("🔗 S'INSCRIRE AVEC DINERO06", url=LIEN_1WIN)],
        [InlineKeyboardButton("✅ J'AI FINI", callback_data="check_sub")]
    ]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(f"Parfait ! Envoie ton **ID 1WIN** (ex: 12345678)", parse_mode="Markdown")

async def handle_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    txt = update.message.text.strip()
    if not txt.isdigit() or not (6 <= len(txt) <= 10):
        await update.message.reply_text("❌ ID invalide. Envoie juste les chiffres.")
        return

    try:
        await context.bot.send_message(chat_id=ADMIN_ID, text=f"🔔 Nouveau joueur DINERO06\n👤 {update.effective_user.first_name} @{update.effective_user.username}\n🆔 ID 1WIN: {txt}\nTelegram ID: {user_id}")
    except: pass

    verified_users.add(user_id)
    
    # BOUTON MINI APP ICI
    keyboard = [
        [InlineKeyboardButton("🚀 OUVRIR DINERO APP", web_app=WebAppInfo(url=WEBAPP_URL))],
        [InlineKeyboardButton("🎯 SIGNAL TEXTE", callback_data="signal")]
    ]
    await update.message.reply_text(
        f"✅ ID **{txt}** vérifié !\n\n🔓 **Accès Mini App débloqué** 👇", 
        reply_markup=InlineKeyboardMarkup(keyboard), 
        parse_mode="Markdown"
    )

async def signal_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    if q:
        await q.answer()
        uid = q.from_user.id
        sender = q.message.reply_text
    else:
        uid = update.effective_user.id
        sender = update.message.reply_text
    
    if uid not in verified_users:
        await sender(f"❌ Inscris-toi d'abord. Tape /start")
        return

    now = datetime.now()
    target = now + timedelta(minutes=3)
    cote = round(random.uniform(2.5, 8.5), 2)
    msg = f"✈️ **SIGNAL DINERO06** ✈️\n\n🕒 Heure : **{target.strftime('%H:%M:%S')}**\n📈 Cote : **x{cote}**\n💰 Mise : 1000F"
    
    keyboard = [
        [InlineKeyboardButton("🚀 OUVRIR DINERO APP", web_app=WebAppInfo(url=WEBAPP_URL))],
        [InlineKeyboardButton("🎯 NOUVEAU SIGNAL", callback_data="signal")]
    ]
    await sender(msg, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

def main():
    # Lance Flask dans un thread
    threading.Thread(target=run_flask, daemon=True).start()
    
    # Lance le bot
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signal", signal_handler))
    app.add_handler(CallbackQueryHandler(handle_callback, pattern="check_sub"))
    app.add_handler(CallbackQueryHandler(signal_handler, pattern="signal"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_id))
    print("DINERO BOT + MINI APP démarrés...")
    app.run_polling()

if __name__ == "__main__":
    main()
