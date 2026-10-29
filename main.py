import asyncio
import os
from datetime import datetime, timedelta
import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

# --- CONFIG DINERO BOT - SEKOU ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
PROMO_CODE = "DINERO06"
LIEN_1WIN = "https://1win.ci/betting?p=unoe&sharebet=DINERO06"
ADMIN_ID = 6312211592
verified_users = set()
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        f"👋 Salut ! Bienvenue sur **DINERO BOT** 🔥\n\n"
        f"Pour débloquer les prédictions, inscris-toi avec mon code officiel :\n\n"
        f"🔥 CODE : **{PROMO_CODE}** 🔥\n\n"
        f"1️⃣ Clique ci-dessous pour t'inscrire\n"
        f"2️⃣ Crée ton compte avec **{PROMO_CODE}**\n"
        f"3️⃣ Envoie ton ID 1WIN ici\n"
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
        await update.message.reply_text("❌ ID invalide. Envoie juste les chiffres de ton ID 1WIN")
        return

    # Envoie l'ID au admin (toi)
    try:
        await context.bot.send_message(chat_id=ADMIN_ID, text=f"🔔 Nouveau joueur DINERO06\n👤 {update.effective_user.first_name} @{update.effective_user.username}\n🆔 ID 1WIN: {txt}\nTelegram ID: {user_id}")
    except: pass

    verified_users.add(user_id)
    await update.message.reply_text(f"✅ ID **{txt}** vérifié ! Code **{PROMO_CODE}** validé.\n\nTape /signal pour ton prédiction 🚀", parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎯 SIGNAL", callback_data="signal")]]))

async def signal_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        q = update.callback_query
        await q.answer()
        uid = q.from_user.id
        sender = q.message.reply_text
    else:
        uid = update.effective_user.id
        sender = update.message.reply_text
    
    if uid not in verified_users:
        await sender(f"❌ Inscris-toi d'abord avec {PROMO_CODE}. Tape /start")
        return

    now = datetime.now()
    target = now + timedelta(minutes=3)
    cote = round(random.uniform(1.9, 6.2), 2)
    msg = f"✈️ **SIGNAL DINERO06** ✈️\n\n🕒 Heure : **{target.strftime('%H:%M:%S')}**\n📈 Cote : **x{cote}**\n\n💰 Mise : 1000F\n🛑 Cashout auto à x{cote}\n\nCode : {PROMO_CODE}"
    await sender(msg, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎯 NOUVEAU SIGNAL", callback_data="signal")]]), parse_mode="Markdown")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signal", signal_handler))
    app.add_handler(CallbackQueryHandler(handle_callback, pattern="check_sub"))
    app.add_handler(CallbackQueryHandler(signal_handler, pattern="signal"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_id))
    app.run_polling()

if __name__ == "__main__":
    main()
