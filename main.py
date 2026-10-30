import os
import telebot
from telebot import types

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

LINK_1WIN = "https://1win.ci/betting?p=unoe&sharebet=DINERO06"
CODE_PROMO = "DINERO06"

@bot.message_handler(commands=['start'])
def start(message):
    nom = message.from_user.first_name
    text = (
        f"👋 Bienvenue {nom} sur DINERO06 !\n\n"
        "🎰 Obtenez des prédictions exclusives pour gagner sur 1Win.\n\n"
        "📋 Que souhaitez-vous faire ?"
    )
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(
        types.KeyboardButton("🎰 S'inscrire sur 1Win"),
        types.KeyboardButton("❓ Comment ça marche ?"),
        types.KeyboardButton("✅ Déjà inscrit(e)"),
        types.KeyboardButton("🏆 ACCÉDER AUX PRÉDICTIONS")
    )
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "🎰 S'inscrire sur 1Win")
def inscrire(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔗 S'inscrire maintenant", url=LINK_1WIN))
    bot.send_message(
        message.chat.id,
        f"1️⃣ Clique sur le lien ci-dessous\n2️⃣ Inscris-toi avec le code promo {CODE_PROMO}\n3️⃣ Dépose 3000F minimum",
        reply_markup=markup
    )

@bot.message_handler(func=lambda m: m.text == "❓ Comment ça marche ?")
def how(message):
    text = (
        "📋 COMMENT ÇA MARCHE ?\n\n"
        f"1️⃣ Inscrivez-vous sur 1Win avec le code promo {CODE_PROMO}\n\n"
        "2️⃣ Déposez minimum 3000 FCFA sur votre compte 1Win\n\n"
        "3️⃣ Revenez ici et cliquez sur \"ACCÉDER AUX PRÉDICTIONS\"\n\n"
        "4️⃣ Accédez gratuitement aux prédictions exclusives !\n\n"
        "⚠️ Le dépôt est vérifié automatiquement. L'accès est accordé dès que le dépôt minimum est atteint."
    )
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🎰 S'inscrire sur 1Win", url=LINK_1WIN))
    markup.add(types.InlineKeyboardButton("⬅️ Retour", callback_data="back"))
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.message_handler(func=lambda m: m.text in ["✅ Déjà inscrit(e)", "🏆 ACCÉDER AUX PRÉDICTIONS"])
def acces(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("✅ Vérifier mon dépôt", url=LINK_1WIN))
    bot.send_message(
        message.chat.id,
        f"Pour accéder aux prédictions, assure-toi d'avoir utilisé le code {CODE_PROMO} et déposé 3000F minimum.\n\nEnvoie ton ID 1Win ici 👇",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "back")
def back(call):
    start(call.message)

print("Bot lancé...")
bot.infinity_polling()
