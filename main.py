import os, time, threading, telebot
from telebot import types
from flask import Flask, send_from_directory

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
LIEN = "https://1win.ci/betting?p=unoe&sharebet=DINERO06"
CODE = "DINERO06"
# Mets ton propre ID Telegram ici pour recevoir les demandes - tape /myid sur @userinfobot
ADMIN_ID = 123456789 # REMPLACE PAR TON ID
users_verifies = {}
pending = {}

app = Flask(__name__)
@app.route('/')
def index(): return send_from_directory('.', 'index.html')
@app.route('/<path:path>')
def serve_static(path): return send_from_directory('.', path)
def run_flask(): app.run(host='0.0.0.0', port=int(os.environ.get("PORT",10000)))

@bot.message_handler(commands=['start','myid'])
def start(message):
    if message.text.startswith('/myid'):
        bot.send_message(message.chat.id, f"Ton ID est: {message.chat.id}")
        return
    text = f"👋 Bienvenue {message.from_user.first_name} sur {CODE} !\n\n🎰 Obtenez des prédictions exclusives pour gagner sur 1Win.\n\n📋 Que souhaitez-vous faire ?"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add("🎰 S'inscrire sur 1Win","❓ Comment ça marche ?","✅ Déjà inscrit(e)","🏆 ACCÉDER AUX PRÉDICTIONS")
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "🎰 S'inscrire sur 1Win")
def inscrire(m):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🌐 S'inscrire avec DINERO06", url=LIEN))
    markup.add(types.InlineKeyboardButton("⬅️ Retour", callback_data="retour"))
    bot.send_message(m.chat.id, f"👉 Lien officiel avec ton code:\n{LIEN}\n\nCode: {CODE}\nDépôt minimum: 3000F", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "❓ Comment ça marche ?")
def how(m):
    bot.send_message(m.chat.id, f"📋 COMMENT ÇA MARCHE ?\n\n1️⃣ Inscris-toi via ce lien: {LIEN}\n2️⃣ Code promo: {CODE}\n3️⃣ Dépose 3000F\n4️⃣ Clique sur 'Déjà inscrit' et envoie ton ID + capture d'écran de ton profil 1Win montrant le code.")

# --- CORRECTION PROBLÈME 1 ---
@bot.message_handler(func=lambda m: m.text == "✅ Déjà inscrit(e)")
def deja(m):
    if m.chat.id in users_verifies:
        vip(m.chat.id)
    else:
        bot.send_message(m.chat.id, "✅ Parfait !\n\nEnvoie ton ID 1Win ET une capture d'écran de ton profil 1Win où on voit le code promo DINERO06.\n\nTon ID se trouve dans ton profil 1Win.")

@bot.message_handler(func=lambda m: m.text == "🏆 ACCÉDER AUX PRÉDICTIONS")
def acceder(m):
    if m.chat.id in users_verifies:
        vip(m.chat.id)
    else:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🌐 S'inscrire sur 1Win", url=LIEN))
        bot.send_message(m.chat.id, f"❌ Vous n'êtes pas encore inscrit(e).\n\nVeuillez vous inscrire d'abord sur 1Win avec le code promo {CODE}.", reply_markup=markup)

@bot.message_handler(content_types=['text','photo'])
def verif(m):
    if m.text and m.text.isdigit() and len(m.text)>=6:
        pending[m.chat.id]=m.text
        bot.send_message(m.chat.id, f"⏳ ID {m.text} reçu !\n\n🔍 Vérification en cours...\nNotre équipe vérifie dans 1Win Partners si tu as bien utilisé {CODE} et déposé 3000F.\n\nTu seras notifié dans 5-10 minutes. Ne renvoie pas ton ID.")
        # Envoie à l'admin (toi)
        try:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("✅ APPROUVER", callback_data=f"approve_{m.chat.id}"),
                       types.InlineKeyboardButton("❌ REFUSER", callback_data=f"deny_{m.chat.id}"))
            bot.send_message(ADMIN_ID, f"🔔 NOUVELLE DEMANDE\nID 1Win: {m.text}\nUser Telegram: {m.chat.id}\nCode: {CODE}", reply_markup=markup)
        except:
            pass
        print(f"ID A VERIFIER: {m.text} de {m.chat.id}")
    elif m.content_type=='photo':
        bot.send_message(m.chat.id, "✅ Capture reçue ! Merci. Garde ton ID sous la main, on vérifie ton compte.")

def vip(chat_id):
    url = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME','ton-site.onrender.com')}/"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🎮 Accéder aux Prédictions", web_app=types.WebAppInfo(url=url)))
    bot.send_message(chat_id, f"🏆 FÉLICITATIONS - ACCÈS VIP\n\nTu as accès aux prédictions {CODE} !", reply_markup=markup)

@bot.callback_query_handler(func=lambda c: True)
def cb(c):
    if c.data=="retour": start(c.message)
    if c.data.startswith("approve_"):
        uid=int(c.data.split("_")[1])
        users_verifies[uid]=pending.get(uid,"")
        bot.send_message(uid, "✅ Vérification réussie ! Ton compte avec DINERO06 est confirmé. Clique pour accéder aux prédictions:")
        vip(uid)
        bot.answer_callback_query(c.id, "Approuvé !")
    if c.data.startswith("deny_"):
        uid=int(c.data.split("_")[1])
        bot.send_message(uid, f"❌ Vérification échouée. On ne voit pas le code {CODE} ou le dépôt de 3000F sur ton ID. Vérifie et renvoie.")
        bot.answer_callback_query(c.id, "Refusé")
    bot.answer_callback_query(c.id)

threading.Thread(target=run_flask,daemon=True).start()
bot.infinity_polling()
