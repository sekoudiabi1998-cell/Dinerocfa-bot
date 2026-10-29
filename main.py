import os
import threading
from flask import Flask, send_from_directory
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, WebAppInfo, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
PROMO_CODE = "DINERO06"
LIEN_1WIN = "https://1win.ci/betting?p=unoe&sharebet=DINERO06"
ADMIN_ID = 6312211592
WEBAPP_URL = "https://dinerocfa-bot.onrender.com"

verified_users = set()
pending_users = {}

app_flask = Flask(__name__)
@app_flask.route('/')
def index(): return send_from_directory('.', 'index.html')
@app_flask.route('/<path:path>')
def static_files(path): return send_from_directory('.', path)
def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host="0.0.0.0", port=port)

def get_main_menu():
    keyboard = [
        [KeyboardButton("🎰 S'inscrire sur 1Win")],
        [KeyboardButton("❓ Comment ça marche ?")],
        [KeyboardButton("✅ Déjà inscrit(e)")],
        [KeyboardButton("🏆 ACCÉDER AUX PRÉDICTIONS")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name
    text = f"👋 Bienvenue {name} sur **{PROMO_CODE}** !\n\n🎰 Obtenez des prédictions exclusives pour gagner sur 1Win.\n\n📋 Que souhaitez-vous faire ?"
    await update.message.reply_text(text, reply_markup=get_main_menu(), parse_mode="Markdown")

async def retour_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    name = q.from_user.first_name
    text = f"👋 Re-bienvenue {name} sur **{PROMO_CODE}** !\n\n🎰 Obtenez des prédictions exclusives pour gagner sur 1Win.\n\n📋 Que souhaitez-vous faire ?"
    await q.message.delete()
    await context.bot.send_message(chat_id=q.from_user.id, text=text, reply_markup=get_main_menu(), parse_mode="Markdown")

async def handle_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    txt = update.message.text.strip()
    name = update.effective_user.first_name

    if "S'inscrire" in txt:
        kb = [[InlineKeyboardButton("🔗 S'INSCRIRE AVEC DINERO06", url=LIEN_1WIN)]]
        await update.message.reply_text(f"🔥 Clique ici avec le code **{PROMO_CODE}** :\n\n👉 {LIEN_1WIN}", reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

    elif "Comment ça marche" in txt:
        await update.message.reply_text(f"❓ **Comment ça marche ?**\n\n1️⃣ Inscris-toi sur 1Win avec {PROMO_CODE}\n2️⃣ Clique ✅ Déjà inscrit(e) et envoie ton ID\n3️⃣ Si ton ID a bien {PROMO_CODE}, accès direct à la Mini App avec 15 jeux", parse_mode="Markdown")

    elif "Déjà inscrit" in txt:
        kb = [[InlineKeyboardButton("➡️ Retour", callback_data="retour_menu")]]
        await update.message.reply_text("Veuillez envoyer votre **ID 1Win** pour vérifier votre inscription.\n\nVotre ID 1Win se trouve dans votre profil 1Win.", reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

    elif "ACCÉDER AUX PRÉDICTIONS" in txt:
        if uid not in verified_users:
            kb = [[InlineKeyboardButton("➡️ Retour", callback_data="retour_menu")]]
            await update.message.reply_text(f"🔒 Accès refusé. Envoie d'abord ton ID via ✅ Déjà inscrit(e)\n\nTon ID doit avoir été créé avec {PROMO_CODE}", reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")
            return
        kb = [[InlineKeyboardButton("🚀 OUVRIR DINERO MULTI-GAMES", web_app=WebAppInfo(url=WEBAPP_URL))]]
        await update.message.reply_text("🔓 Accès autorisé !", reply_markup=InlineKeyboardMarkup(kb))

    elif txt.isdigit() and 6 <= len(txt) <= 10:
        # Si déjà vérifié
        if uid in verified_users:
            kb = [[InlineKeyboardButton("🚀 OUVRIR DINERO MULTI-GAMES", web_app=WebAppInfo(url=WEBAPP_URL))]]
            await update.message.reply_text("✅ Tu es déjà vérifié !", reply_markup=InlineKeyboardMarkup(kb))
            return
        
        # === ICI LE MESSAGE COMME SULTAN POUR FAUX ID ===
        pending_users[uid] = txt
        kb = [[InlineKeyboardButton("➡️ Retour", callback_data="retour_menu")]]
        await update.message.reply_text(
            f"❌ ID 1Win {txt} non trouvé dans notre base de données.\n\nVérifiez que vous avez utilisé le code promo **{PROMO_CODE}** lors de votre inscription sur 1Win.",
            reply_markup=InlineKeyboardMarkup(kb),
            parse_mode="Markdown"
        )
        # Notifie l'admin pour que tu puisses approuver manuellement le vrai ID
        try:
            kb_admin = [[InlineKeyboardButton(f"✅ APPROUVER {txt}", callback_data=f"approve_{uid}"), InlineKeyboardButton(f"❌ REFUSER", callback_data=f"reject_{uid}")]]
            await context.bot.send_message(chat_id=ADMIN_ID, text=f"🔔 ID à vérifier\n👤 {name} @{update.effective_user.username}\n🆔 {txt}\nTG: {uid}", reply_markup=InlineKeyboardMarkup(kb_admin))
        except: pass

async def admin_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    if q.from_user.id != ADMIN_ID: return
    await q.answer()
    target_id = int(q.data.split("_")[1])
    onewin = pending_users.get(target_id, "")
    if q.data.startswith("approve_"):
        verified_users.add(target_id)
        kb = [[InlineKeyboardButton("🚀 OUVRIR DINERO MULTI-GAMES", web_app=WebAppInfo(url=WEBAPP_URL))]]
        try: await context.bot.send_message(chat_id=target_id, text=f"✅ ID {onewin} validé ! Ton accès est débloqué.", reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")
        except: pass
        await q.message.reply_text(f"✅ {onewin} approuvé")
    else:
        await q.message.reply_text(f"❌ {onewin} refusé")

def main():
    threading.Thread(target=run_flask, daemon=True).start()
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(retour_menu, pattern="retour_menu"))
    app.add_handler(CallbackQueryHandler(admin_callback, pattern="^(approve_|reject_)"))
    app.add_handler(MessageHandler(filters.TEXT, handle_menu))
    app.run_polling()

if __name__ == "__main__": main()
