import os
import threading
from flask import Flask, send_from_directory
from telegram import KeyboardButton, ReplyKeyboardMarkup, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
WEBAPP_URL = "https://dinerocfa-bot.onrender.com"
LINK_1WIN = "https://1win.ci/betting?p=unoe&sharebet=DINERO06"
CODE_PROMO = "DINERO06"

flask_app = Flask(__name__)
@flask_app.route('/')
def home():
    return send_from_directory('.', 'index.html')

def run_flask():
    flask_app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

# 1. /start - comme image 1
async def start(update: ContextTypes.DEFAULT_TYPE, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["awaiting_id"] = False
    name = update.effective_user.first_name or "DIABI"
    text = f"👋 Bienvenue {name} sur DINERO CFA !\n\n🎰 Obtenez des prédictions exclusives pour gagner sur 1Win.\n\n📋 Que souhaitez-vous faire ?"
    keyboard = [
        [KeyboardButton(text="🎰 S'inscrire sur 1Win")],
        [KeyboardButton(text="❓ Comment ça marche ?")],
        [KeyboardButton(text="✅ Déjà inscrit(e)")],
        [KeyboardButton(text="🏆 ACCÉDER AUX PRÉDICTIONS", web_app=WebAppInfo(url=WEBAPP_URL))]
    ]
    await update.message.reply_text(text, reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))

# 2. Gestion de tous les boutons - comme images 1,2,3
async def handle_buttons(update: ContextTypes.DEFAULT_TYPE, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text or ""
    
    # Si on attend un ID 1Win
    if context.user_data.get("awaiting_id"):
        if msg.isdigit() and len(msg) >= 6:
            # Image 2 et 3 - Félicitations
            context.user_data["awaiting_id"] = False
            text = f"🏆 FÉLICITATIONS - ACCÈS VIP\n\nVous avez accès aux prédictions exclusives {CODE_PROMO} !\n\n👉 Cliquez sur le bouton ci-dessous pour accéder :"
            kb = [[KeyboardButton(text="🎮 Accéder aux Prédictions", web_app=WebAppInfo(url=WEBAPP_URL))]]
            await update.message.reply_text(text, reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True))
            return
        elif "Retour" not in msg:
            await update.message.reply_text("ID invalide. Envoyez uniquement votre ID 1Win (ex: 385943982).")
            return

    if "S'inscrire" in msg:
        kb = [[InlineKeyboardButton(f"S'inscrire avec {CODE_PROMO}", url=LINK_1WIN)]]
        await update.message.reply_text(
            f"Pour activer les signaux DINERO, créez votre compte ici :\n\n{Link_1Win if False else LINK_1WIN}\n\nCode promo obligatoire : {CODE_PROMO}\nBonus 500% activé.",
            reply_markup=InlineKeyboardMarkup(kb)
        )
    elif "Comment" in msg:
        await update.message.reply_text(
            f"❓ COMMENT ÇA MARCHE ?\n\n"
            f"1. Inscris-toi ici : {LINK_1WIN}\n"
            f"2. Code promo : {CODE_PROMO}\n"
            f"3. Dépose minimum 3000F\n"
            f"4. Envoie ton ID 1Win ici pour vérification\n"
            f"5. Accède aux 15 jeux DINERO CFA"
        )
    elif "Déjà" in msg:
        context.user_data["awaiting_id"] = True
        kb = [[KeyboardButton(text="⬅️ Retour")]]
        await update.message.reply_text(
            "Veuillez envoyer votre ID 1Win pour vérifier votre inscription.\n\nVotre ID 1Win se trouve dans votre profil 1Win.",
            reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True)
        )
    elif "Retour" in msg:
        await start(update, context)

def run_bot():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))
    app.run_polling()

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    run_bot()
