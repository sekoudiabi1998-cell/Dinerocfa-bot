import os, threading, asyncio
from flask import Flask, send_from_directory
from telegram import KeyboardButton, ReplyKeyboardMarkup, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
WEBAPP_URL = "https://dinerocfa-bot.onrender.com"
LINK_1WIN = "https://1win.ci/betting?p=unoe&sharebet=DINERO06"
CODE = "DINERO06"

# === TON ID TEST EST DEBLOQUE ===
VALID_IDS = {"385943982"}

flask_app = Flask(__name__)
@flask_app.route('/')
def home():
    return send_from_directory('.', 'index.html')
def run_flask():
    flask_app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

async def start(update, context):
    context.user_data.clear()
    name = update.effective_user.first_name or "DIABI"
    text = f"👋 Bienvenue {name} sur DINERO CFA !\n\n🎰 Obtenez des prédictions exclusives pour gagner sur 1Win avec le code {CODE}.\n\n📋 Que souhaitez-vous faire ?"
    kb = [
        [KeyboardButton(text="🎰 S'inscrire sur 1Win")],
        [KeyboardButton(text="❓ Comment ça marche ?")],
        [KeyboardButton(text="✅ Déjà inscrit(e)")],
        [KeyboardButton(text="🏆 ACCÉDER AUX PRÉDICTIONS", web_app=WebAppInfo(url=WEBAPP_URL))]
    ]
    await update.message.reply_text(text, reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True))

async def handle_buttons(update, context):
    msg = (update.message.text or "").strip()

    if "⬅️ Retour" in msg or msg.lower() == "retour":
        await start(update, context)
        return

    if "Déjà" in msg:
        context.user_data["awaiting_id"] = True
        await update.message.reply_text(
            "Veuillez envoyer votre ID 1Win pour vérifier votre inscription.\n\nVotre ID 1Win se trouve dans votre profil 1Win.",
            reply_markup=ReplyKeyboardMarkup([[KeyboardButton(text="⬅️ Retour")]], resize_keyboard=True)
        )
        return

    # === RECEPTION DE L'ID ===
    if context.user_data.get("awaiting_id") and msg.isdigit() and len(msg) >= 6:
        await update.message.reply_text(f"🔍 Vérification de l'ID {msg} avec code {CODE}...")
        await asyncio.sleep(2)
        
        if msg in VALID_IDS:
            context.user_data["verified"] = True
            context.user_data["awaiting_id"] = False
            text = f"🏆 FÉLICITATIONS - ACCÈS VIP\n\nVous avez accès aux prédictions exclusives DINERO06 !\n\n👉 Cliquez sur le bouton ci-dessous pour accéder :"
            kb = [[KeyboardButton(text="🎮 Accéder aux Prédictions", web_app=WebAppInfo(url=WEBAPP_URL))]]
            await update.message.reply_text(text, reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True))
        else:
            kb = [
                [InlineKeyboardButton(f"🔗 S'inscrire avec {CODE}", url=LINK_1WIN)],
                [InlineKeyboardButton("🔄 J'ai rechargé, revérifier", callback_data=f"recheck_{msg}")]
            ]
            await update.message.reply_text(
                f"❌ ID {msg} REFUSÉ\n\n"
                f"Aucun dépôt de 3000F trouvé sur un compte créé avec {CODE}.\n\n"
                f"👉 Pour débloquer :\n"
                f"1. Clique en bas et crée un NOUVEAU compte\n"
                f"2. Code promo obligatoire : {CODE}\n"
                f"3. Recharge 3000F\n"
                f"4. Reviens avec ton nouvel ID",
                reply_markup=InlineKeyboardMarkup(kb)
            )
        return

    if "S'inscrire" in msg:
        kb = [[InlineKeyboardButton(f"S'inscrire avec {CODE} - Bonus 500%", url=LINK_1WIN)]]
        await update.message.reply_text(f"Lien officiel DINERO CFA :\n{LINK_1WIN}\n\nCode : {CODE}", reply_markup=InlineKeyboardMarkup(kb))
    
    elif "Comment" in msg:
        await update.message.reply_text(
            f"❓ COMMENT ÇA MARCHE ?\n\n"
            f"1. Inscris-toi ici : {LINK_1WIN}\n"
            f"2. Code promo : {CODE}\n"
            f"3. Dépose minimum 3000F\n"
            f"4. Envoie ton ID 1Win\n"
            f"5. Accès aux 15 jeux DINERO CFA"
        )
    
    elif "ACCÉDER" in msg:
        if not context.user_data.get("verified"):
            await update.message.reply_text("⛔ ACCÈS REFUSÉ\n\nVérifie d'abord ton ID.\nClique sur ✅ Déjà inscrit(e)")
            return

async def addid(update, context):
    if not context.args:
        await update.message.reply_text("Utilisation : /addid 12345678")
        return
    VALID_IDS.add(context.args[0])
    await update.message.reply_text(f"✅ ID {context.args[0]} ajouté à la liste VIP DINERO CFA !")

async def cb(update, context):
    q = update.callback_query
    await q.answer()
    await q.message.reply_text("Vérification... Toujours pas de dépôt trouvé. Assure-toi d'avoir utilisé le lien DINERO06.")

def run_bot():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("addid", addid))
    app.add_handler(CallbackQueryHandler(cb))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))
    app.run_polling()

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    run_bot()
