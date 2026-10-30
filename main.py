import os
import time
import threading
import telebot
from telebot import types
from flask import Flask, send_from_directory

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

LIEN = "https://1win.ci/betting?p=unoe&sharebet=DINERO06"
CODE = "DINERO06"

# Stockage des gens qui ont envoyé leur ID
users_verifies = {}

# --- SERVEUR POUR LA MINI-APP ---
app = Flask(__name__)
@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- BOT TELEGRAM ---

@bot.message_handler(commands=['start'])
def start(message):
    nom = message.from_user.first_name
    text = f"👋 Bienvenue {nom} sur {CODE} !\n\n🎰 Obtenez des prédictions exclusives pour gagner sur 1Win.\n\n📋 Que souhaitez-vous faire ?"
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
    markup.add(types.InlineKeyboardButton("🌐 S'inscrire sur 1Win", url=LIEN))
    markup.add(types.InlineKeyboardButton("⬅️ Retour", callback_data="retour"))
    bot.send_message(message.chat.id, f"Voici ton lien officiel :\n{LIEN}\n\nCode promo: {CODE}\nDépôt minimum: 3000 FCFA", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "❓ Comment ça marche ?")
def comment_marche(message):
    text = (
        f"📋 COMMENT ÇA MARCHE ?\n\n"
        f"1️⃣ Inscris-toi sur 1Win avec le code promo {CODE}\n"
        f"2️⃣ Dépose minimum 3000 FCFA\n"
        f"3️⃣ Envoie ton ID 1Win ici\n"
        f"4️⃣ Accès débloqué aux prédictions !\n\n"
        f"Lien: {LIEN}"
    )
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🌐 S'inscrire sur 1Win", url=LIEN))
    markup.add(types.InlineKeyboardButton("⬅️ Retour", callback_data="retour"))
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.message_handler(func=lambda m: m.text in ["✅ Déjà inscrit(e)", "🏆 ACCÉDER AUX PRÉDICTIONS"])
def demander_id(message):
    if message.chat.id in users_verifies:
        envoyer_acces_vip(message.chat.id)
    else:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🌐 S'inscrire sur 1Win", url=LIEN))
        markup.add(types.InlineKeyboardButton("⬅️ Retour", callback_data="retour"))
        bot.send_message(
            message.chat.id,
            f"❌ Vous n'êtes pas encore inscrit(e).\n\nVeuillez vous inscrire d'abord sur 1Win avec le code promo {CODE}.",
            reply_markup=markup
        )
        time.sleep(1)
        bot.send_message(
            message.chat.id,
            "Veuillez envoyer votre ID 1Win pour vérifier votre inscription.\n\nVotre ID 1Win se trouve dans votre profil 1Win."
        )

@bot.message_handler(func=lambda m: m.text and m.text.isdigit() and len(m.text) >= 6)
def verification_id(message):
    id_1win = message.text
    users_verifies[message.chat.id] = id_1win
    print(f"NOUVEL ID A VERIFIER: {id_1win} user {message.chat.id}")
    bot.send_message(message.chat.id, f"ID {id_1win} reçu. Vérification...")
    time.sleep(2)
    envoyer_acces_vip(message.chat.id)

def envoyer_acces_vip(chat_id):
    text = (
        f"🏆 FÉLICITATIONS - ACCÈS VIP\n\n"
        f"Vous avez accès aux prédictions exclusives {CODE} !\n\n"
        f"👉 Cliquez sur le bouton ci-dessous pour accéder :"
    )
    # Le bouton ouvre la mini-app (ton URL Render)
    mini_app_url = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME', 'ton-site.onrender.com')}/"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🎮 Accéder aux Prédictions", web_app=types.WebAppInfo(url=mini_app_url)))
    bot.send_message(chat_id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callbacks(call):
    if call.data == "retour":
        start(call.message)
    bot.answer_callback_query(call.id)

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    print(f"Bot {CODE} lancé avec {LIEN}")
    bot.infinity_polling()
