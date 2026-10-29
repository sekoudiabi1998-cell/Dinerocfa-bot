from telegram import KeyboardButton, ReplyKeyboardMarkup, WebAppInfo, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os

TOKEN = os.getenv("BOT_TOKEN")
WEBAPP_URL = "https://ton-lien-render.onrender.com"  # <-- METS TON LIEN RENDER ICI

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton(text="🏆 ACCÉDER AUX PRÉDICTIONS", web_app=WebAppInfo(url=WEBAPP_URL))]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "👋 Bienvenue DIABI sur DINERO06 !\n\n"
        "🎰 Obtenez des prédictions exclusives pour gagner sur 1Win.\n\n"
        "📋 Que souhaitez-vous faire ?",
        reply_markup=reply_markup
    )

# Si quelqu'un tape le texte du bouton, on ouvre aussi directement
async def handle_access(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "ACCÉDER" in update.message.text:
        # On renvoie le même bouton webapp directement, pas de 2ème étape
        keyboard = [
            [KeyboardButton(text="🏆 ACCÉDER AUX PRÉDICTIONS", web_app=WebAppInfo(url=WEBAPP_URL))]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("🔓 Accès autorisé ! Clique en bas pour ouvrir.", reply_markup=reply_markup)

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_access))
app.run_polling()
