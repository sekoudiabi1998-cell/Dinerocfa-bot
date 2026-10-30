from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "9260749069:AAGfHUXEXVdKm5Rpr1-RWG2eh5_8_HUciXo"
WEBAPP_URL = "https://dinerocfa-bot.onrender.com"
PROMO = "DINERO06"

user_step = {}

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    txt = f"👋 Bienvenue {user} sur {PROMO} !\n\n🎰 Obtenez des prédictions exclusives pour gagner sur 1Win.\n\n📋 Que souhaitez-vous faire ?"
    kb = [
        [InlineKeyboardButton("🎰 S'inscrire sur 1Win", url=f"https://1win.ci/betting?p=unoe&sharebet={PROMO}")],
        [InlineKeyboardButton("❓ Comment ça marche ?", callback_data="how")],
        [InlineKeyboardButton("✅ Déjà inscrit(e)", callback_data="already")],
        [InlineKeyboardButton("🏆 ACCÉDER AUX PRÉDICTIONS", callback_data="access_direct")]
    ]
    await update.message.reply_text(txt, reply_markup=InlineKeyboardMarkup(kb))

async def btn(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    uid = q.from_user.id
    await q.answer()
    
    if q.data == "how":
        await q.message.reply_text(f"1️⃣ Inscris-toi avec {PROMO}\n2️⃣ Recharge 500F\n3️⃣ Envoie ton ID 1Win\n4️⃣ Accède aux signaux")
    
    elif q.data == "already":
        user_step[uid] = "wait_id"
        await q.message.reply_text(
            "Veuillez envoyer votre ID 1Win pour vérifier votre inscription.\n\nVotre ID 1Win se trouve dans votre profil 1Win.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Retour", callback_data="retour")]])
        )
    
    elif q.data == "access_direct":
        # ANTI-TRICHE IMAGE 2 : bloque si pas vérifié
        if user_step.get(uid) != "verified":
            kb = [
                [InlineKeyboardButton("🌐 S'inscrire sur 1Win", url=f"https://1win.ci/betting?p=unoe&sharebet={PROMO}")],
                [InlineKeyboardButton("⬅️ Retour", callback_data="retour")]
            ]
            await q.message.reply_text(
                f"❌ Vous n'êtes pas encore inscrit(e).\n\nVeuillez vous inscrire d'abord sur 1Win avec le code promo {PROMO}.",
                reply_markup=InlineKeyboardMarkup(kb)
            )
        else:
            kb = [[InlineKeyboardButton("🎮 Accéder aux Prédictions", web_app=WebAppInfo(url=WEBAPP_URL))]]
            await q.message.reply_text(f"🏆 FÉLICITATIONS - ACCÈS VIP\n\nVous avez accès aux prédictions exclusives {PROMO} !", reply_markup=InlineKeyboardMarkup(kb))

    elif q.data == "retour":
        user_step.pop(uid, None)
        await start(update, ctx)

async def id_handler(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if user_step.get(uid) != "wait_id":
        return
    if not update.message.text.isdigit():
        await update.message.reply_text("❌ Envoie seulement ton ID numérique 1Win")
        return
    
    user_step[uid] = "verified"
    kb = [[InlineKeyboardButton("🎮 Accéder aux Prédictions", web_app=WebAppInfo(url=WEBAPP_URL))]]
    await update.message.reply_text(
        f"🏆 FÉLICITATIONS - ACCÈS VIP\n\nVous avez accès aux prédictions exclusives {PROMO} !\n\n👉 Cliquez sur le bouton ci-dessous pour accéder :",
        reply_markup=InlineKeyboardMarkup(kb)
    )

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(btn))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, id_handler))
app.run_polling()
