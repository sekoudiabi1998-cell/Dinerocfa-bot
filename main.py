# Ajoute ça en haut de ton main.py
utilisateurs_verifies = {}  # on stocke qui a envoyé son ID

@bot.message_handler(func=lambda m: m.text == "🏆 ACCÉDER AUX PRÉDICTIONS")
def acces_predictions(message):
    user_id = message.chat.id
    if user_id in utilisateurs_verifies:
        # Il a déjà envoyé son ID, on lui donne les prédictions
        bot.send_message(user_id, "🏆 Voilà tes prédictions du jour !\n\n⚽️ Match: ...\nCote: ...")
    else:
        # Il n'a pas encore prouvé son inscription
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🎰 S'inscrire avec DINERO06", url="https://1win.ci/betting?p=unoe&sharebet=DINERO06"))
        bot.send_message(
            user_id,
            "🔒 ACCÈS BLOQUÉ\n\n"
            "Pour débloquer les prédictions, tu dois :\n"
            f"1️⃣ T'inscrire avec le code {CODE_PROMO}\n"
            "2️⃣ Déposer minimum 3000 FCFA\n"
            "3️⃣ Envoyer ton ID 1Win ici (ex: 12345678)\n\n"
            "Envoie ton ID maintenant 👇",
            reply_markup=markup
        )

@bot.message_handler(func=lambda m: m.text.isdigit() and len(m.text) >= 6)
def verifier_id(message):
    id_1win = message.text
    user_id = message.chat.id
    
    bot.send_message(user_id, f"⏳ Vérification de l'ID {id_1win} en cours...\nJe vérifie si tu as bien utilisé {CODE_PROMO} et déposé 3000F.")

    # Simulation de 2 secondes
    import time
    time.sleep(2)
    
    utilisateurs_verifies[user_id] = id_1win
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🏆 ACCÉDER AUX PRÉDICTIONS MAINTENANT", callback_data="predictions"))
    
    bot.send_message(
        user_id,
        f"✅ ID {id_1win} enregistré !\n\n"
        "Je vérifie ton dépôt dans mon tableau partenaire 1Win.\n"
        "Si ton dépôt de 3000F avec le code DINERO06 est OK, l'accès sera débloqué dans quelques minutes.\n\n"
        "Clique ci-dessous pour réessayer :",
        reply_markup=markup
    )
    # TOI, tu vas recevoir son ID sur Telegram et tu vérifies dans ton app 1Win Partners
    print(f"NOUVEL ID À VÉRIFIER : {id_1win} de l'utilisateur {user_id}")
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
