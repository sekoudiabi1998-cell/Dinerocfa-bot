import os
import time
import telebot
from telebot import types

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

LIEN_INSCRIPTION = "https://1win.ci/betting?p=unoe&sharebet=DINERO06"
CODE_PROMO = "DINERO06"

utilisateurs_verifies = {}

@bot.message_handler(commands=['start'])
def start(message):
    nom = message.from_user.first_name
    text = f"👋 Bienvenue {nom} sur {CODE_PROMO} !\n\n🎰 Prédictions exclusives 1Win.\n\nTon code promo: {CODE_PROMO}\nDépôt minimum: 3000 FCFA"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🎰 S'inscrire sur 1Win")
    markup.add("❓ Comment ça marche ?")
    markup.add("🏆 ACCÉDER AUX PRÉDICTIONS")
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "🎰 S'inscrire sur 1Win")
def inscrire(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔗 S'inscrire avec DINERO06", url=LIEN_INSCRIPTION))
    bot.send_message(message.chat.id, f"Lien: {LIEN_INSCRIPTION}\nCode: {CODE_PROMO}\nDépôt: 3000F minimum", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "❓ Comment ça marche ?")
def how(message):
    text = (
        f"📋 COMMENT ÇA MARCHE ?\n\n"
        f"1️⃣ Inscris-toi sur 1Win avec le code promo {CODE_PROMO}\n"
        f"2️⃣ Dépose minimum 3000 FCFA\n"
        f"3️⃣ Envoie ton ID 1Win ici\n"
        f"4️⃣ Accès débloqué aux prédictions\n\n"
        f"Lien: {LIEN_INSCRIPTION}"
    )
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🎰 S'inscrire maintenant", url=LIEN_INSCRIPTION))
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "🏆 ACCÉDER AUX PRÉDICTIONS")
def acces_predictions(message):
    user_id = message.chat.id
    if user_id in utilisateurs_verifies:
        bot.send_message(user_id, f"🏆 PRÉDICTIONS VIP pour {CODE_PROMO}:\n\n⚽️ Match du jour: Victoire à domicile\nCote: 1.85\n\nBonne chance !")
    else:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🎰 S'inscrire avec DINERO06", url=LIEN_INSCRIPTION))
        bot.send_message(
            user_id,
            f"🔒 ACCÈS BLOQUÉ\n\nPour débloquer:\n1️⃣ Inscris-toi avec {CODE_PROMO}\n2️⃣ Dépose 3000F\n3️⃣ Envoie ton ID 1Win ici (ex: 12345678)\n\nLien: {LIEN_INSCRIPTION}",
            reply_markup=markup
        )

@bot.message_handler(func=lambda m: m.text.isdigit() and len(m.text) >= 6)
def verifier_id(message):
    id_1win = message.text
    user_id = message.chat.id
    bot.send_message(user_id, f"⏳ Vérification ID {id_1win}...\nJe vérifie {CODE_PROMO} + dépôt 3000F.")
    time.sleep(2)
    utilisateurs_verifies[user_id] = id_1win
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🏆 VÉRIFIER ET ACCÉDER", callback_data="predictions"))
    bot.send_message(user_id, f"✅ ID {id_1win} enregistré ! Clique pour accéder:", reply_markup=markup)
    print(f"NOUVEL ID A VERIFIER: {id_1win} de {user_id}")

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "predictions":
        acces_predictions(call.message)

print("Bot DINERO06 lancé...")
bot.infinity_polling()
