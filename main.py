import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import random

TOKEN = os.getenv("BOT_TOKEN")
PROMO = "DINEROCFA225"
LINK = f"https://1wprxx.com/?open=register&p=ik6q&promo={PROMO}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎯 Signal Aviator du Jour", callback_data="signal")],
        [InlineKeyboardButton("🔗 S'inscrire 1WIN - Bonus 500%", url=LINK)],
        [InlineKeyboardButton("🎁 Code Promo", callback_data="promo")]
    ]
    txt = f"""🚀 *DINERO CFA - AVIATOR* 🚀

Salut {update.effective_user.first_name} !

✅ Signaux gratuits chaque heure
✅ Code Promo : `{PROMO}`
✅ Bonus 500% sur 1WIN

👇 Clique ci-dessous :"""
    await update.message.reply_text(txt, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if q.data == "promo":
        await q.message.reply_text(f"🎁 Ton code : *{PROMO}*\n\nInscris-toi ici : {LINK}\n\nTape {PROMO} et reçois 500% de bonus !", parse_mode="Markdown")
    elif q.data == "signal":
        cote = round(random.uniform(2.1, 7.8), 2)
        await q.message.reply_text(f"🔥 *SIGNAL* 🔥\n\n✈️ Prochain : *x{cote}*\n⚠️ Cashout conseillé : *x{round(cote-0.5,2)}*\n\nJoue avec : {LINK}\nCode : {PROMO}", parse_mode="Markdown")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_buttons))
    app.run_polling()

if __name__ == "__main__":
    main()
