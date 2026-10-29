import os
import threading
from flask import Flask, send_from_directory
from telegram import KeyboardButton, ReplyKeyboardMarkup, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters

TOKEN = os.getenv("BOT_TOKEN")
WEBAPP_URL = "https://dinerocfa-bot.onrender.com"
LINK_1WIN = "https://1win.ci/betting?p=unoe&sharebet=DINERO06"

flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return send_from_directory('.', 'index.html')

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host='0.0.0.0', port=port)

async def start(update, context):
    name = update.effective_user.first_name or "DIABI"
    text = f"Bienvenue {name} sur LACOSTE01 !\n\nObtenez des predictions exclusives pour gagner sur 1Win.\n\nQue souhaitez-vous faire ?"
    keyboard = [
        [KeyboardButton(text="S'inscrire sur 1Win")],
        [KeyboardButton(text="Comment ca marche ?")],
        [KeyboardButton(text="Deja inscrit(e)")],
        [KeyboardButton(text="ACCEDER AUX PREDICTIONS", web_app=WebAppInfo(url=WEBAPP_URL))]
    ]
    await update.message.reply_text(text, reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))

async def handle_buttons(update, context):
    msg = update.message.text
    if "S'inscrire" in msg:
        kb = [[InlineKeyboardButton("S'inscrire avec DINERO06", url=LINK_1WIN)]]
        await update.message.reply_text(
            "Pour activer les signaux, cree ton compte 1Win avec le code promo DINERO06 :\n\n"
            f"{LINK_1WIN}\n\nApres depot, reviens et clique ACCEDER.",
            reply_markup=InlineKeyboardMarkup(kb)
        )
    elif "Comment" in msg:
        await update.message.reply_text(
            "COMMENT CA MARCHE ?\n\n"
            "1. Inscris-toi ici : https://1win.ci/betting?p=unoe&sharebet=DINERO06\n"
            "2. Code promo : DINERO06\n"
            "3. Depose minimum 3000F\n"
            "4. Clique ACCEDER AUX PREDICTIONS\n"
            "5. Choisis Aviator, Lucky Jet, Mines..."
        )
    elif "Deja" in msg:
        await update.message.reply_text("Parfait ! Clique sur ACCEDER AUX PREDICTIONS pour commencer a gagner.")

def run_bot():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))
    app.run_polling()

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    run_bot()
