import os, threading
from flask import Flask, send_from_directory
from telegram import KeyboardButton, ReplyKeyboardMarkup, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
WEBAPP_URL = "https://dinerocfa-bot.onrender.com"
LINK_1WIN = "https://1wpt.com"  # <-- mets ton lien d'affiliation 1Win ici

flask_app = Flask(__name__)
@flask_app.route('/')
def home():
    return send_from_directory('.', 'index.html')

def run_flask():
    flask_app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

# MESSAGE /start IDENTIQUE A SULTAN
async def start(update: ContextTypes.DEFAULT_TYPE, context: ContextTypes.DEFAULT_TYPE):
    user_first = update.effective_user.first_name or "DIABI"
    text = (
        f"👋 Bienvenue {user_first} sur LACOSTE01 !\n\n"
        "🎰 Obtenez des prédictions exclusives pour gagner sur 1Win.\n\n"
        "📋 Que souhaitez-vous faire ?"
    )
    # Les 4 boutons exactement comme sur ta capture
    keyboard = [
        [KeyboardButton(text="🎰 S'inscrire sur 1Win")],
        [KeyboardButton(text="❓ Comment ça marche ?")],
        [KeyboardButton(text="✅ Déjà inscrit(e)")],
        [KeyboardButton(text="🏆 ACCÉDER AUX PRÉDICTIONS", web_app=WebAppInfo(url=WEBAPP_URL))]
    ]
    await update.message.reply_text(
        text,
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

# Gère les clics sur les boutons
async def handle_buttons(update, context):
    txt = update.message.text
    if "S'inscrire" in txt:
        kb = [[InlineKeyboardButton("🔗 S'inscrire maintenant", url=LINK_1WIN)]]
        await update.message.reply_text(
            "Pour que les signaux fonctionnent, tu dois créer un nouveau compte 1Win avec notre code promo.\n\n👇 Clique ici :",
            reply_markup=InlineKeyboardMarkup(kb)
        )
    elif "Comment" in txt:
        await update.message.reply_text(
            "❓ COMMENT ÇA MARCHE ?\n\n"
            "1️⃣ Inscris-toi sur 1Win avec notre lien\n"
            "2️⃣ Fais un dépôt minimum de 3000F\n"
            "3️⃣ Clique sur ACCÉDER AUX PRÉDICTIONS\n"
            "4️⃣ Choisis ton jeu (Aviator, Lucky Jet, Mines...)\n"
            "5️⃣ Clique sur PRÉDICTION et joue !\n\n"
            "🎯 Précision 82-95%"
        )
    elif "Déjà" in txt:
        await update.message.reply_text("✅ Parfait ! Tu peux directement accéder aux prédictions en bas 👇")

def run_bot():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))
    # Pour que le bouton ACCÉDER ré-ouvre aussi le /start
    app.add_handler(MessageHandler(filters.Regex("ACCÉDER"), start))
    app.run_polling()

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    run_bot()
