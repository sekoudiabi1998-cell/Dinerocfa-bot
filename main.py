import os, threading, random
from http.server import HTTPServer, BaseHTTPRequestHandler

# MINI-APP AVEC HEURES
HTML_APP = """
<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<style>*{margin:0;padding:0;box-sizing:border-box;font-family:sans-serif}
body{background:#0b0f1a;color:#fff;padding-bottom:80px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;padding:12px}
.card{position:relative;border-radius:18px;background:#151b2c;height:170px;overflow:hidden;border:1px solid #222a40;cursor:pointer}
.badge{position:absolute;top:8px;left:8px;background:#00d084;color:#000;font-size:10px;font-weight:800;padding:4px 8px;border-radius:6px;z-index:2}
.card-content{position:absolute;bottom:8px;left:10px;z-index:2}
.modal{position:fixed;inset:0;background:rgba(0,0,0,0.88);display:none;align-items:center;justify-content:center;z-index:100;padding:20px}
.modal.active{display:flex}
.modal-box{background:#151b2c;border-radius:20px;padding:24px;width:100%;max-width:340px;text-align:center;border:1px solid #2a3556}
.signal{font-size:52px;font-weight:900;color:#00e676;margin:12px 0}
.btn{width:100%;background:#00d084;color:#000;padding:14px;border-radius:12px;font-weight:800;display:block;text-decoration:none;margin-top:12px}
.time-box{background:#0f1423;border:1px dashed #2a3556;border-radius:12px;padding:10px;margin:10px 0}
.nav{position:fixed;bottom:0;left:0;right:0;background:#111726;display:flex;justify-content:space-around;padding:10px 0 20px;border-top:1px solid #1e263d}
</style></head><body>
<div style="padding:14px;display:flex;justify-content:space-between"><span style="color:#4da3ff">Fermer</span><div style="text-align:center"><b>Dinero CFA Multi-Games</b><br><small style="color:#8a94a6">15 jeux disponibles</small></div><span>...</span></div>
<div style="padding:10px 16px;color:#8a94a6;font-size:13px">Choisissez votre jeu. Signal mis à jour chaque minute.</div>
<div class="grid" id="grid"></div>
<div class="nav"><div style="color:#00d084">🎮 Jeux</div><div>🏆 Classement</div><div>👤 Profil</div><div>⚙️ Réglages</div></div>
<div class="modal" id="modal"><div class="modal-box">
<h2 id="mt">AVIATRIX</h2>
<p style="color:#8a94a6;font-size:12px">ID Vérifié • DINEROCFA225</p>
<div class="signal" id="ms">x3.45</div>
<div class="time-box">
<div style="font-size:12px;color:#8a94a6">HEURE POUR JOUER</div>
<div style="font-size:20px;font-weight:800;margin-top:4px" id="mTime">16:35 - 16:37</div>
<div style="font-size:11px;color:#00e676;margin-top:4px">⏰ Dans 2 minutes</div>
</div>
<p style="font-size:13px">Cashout conseillé: <b id="mc" style="color:#fff">x2.95</b><br><small style="color:#8a94a6">Confiance: 92%</small></p>
<a class="btn" href="https://1win.com/?promo=DINEROCFA225" target="_blank">🚀 JOUER MAINTENANT - BONUS 500%</a>
<p style="font-size:10px;color:#5a647a;margin-top:8px">18+ Jeu responsable. Prédiction non garantie.</p>
<button onclick="document.getElementById('modal').classList.remove('active')" style="margin-top:10px;background:none;border:none;color:#8a94a6">Fermer</button>
</div></div>
<script>
const games=[["AVIATRIX","✈️","#4a2bff"],["TO THE MOON","🚀","#0d1a3a"],["ROCKETX","🚀","#3d2b6a"],["SPEED & CASH","🏎️","#0a2a6a"],["AVIATOR","✈️","#ff2b2b"],["LUCKY JET","🛩️","#7a2bff"],["CRASH","💥","#ff8a00"],["JETX","🛫","#2b4aff"],["SPACEMAN","👨‍🚀","#1a1a3a"],["ROCKET QUEEN","👑","#ff2b8a"],["CASH OR CRASH","💰","#2bff8a"],["BIG BASS CRASH","🎣","#2b8aff"],["CRICKET X","🏏","#3aff2b"],["AVIATRIX 2","✈️","#ff2b4a"],["LIMO","🚗","#ffaa00"]];
const grid=document.getElementById('grid');
function getPlayTime(){
  const now=new Date();const add=Math.floor(Math.random()*8)+2;
  const start=new Date(now.getTime()+add*60000);const end=new Date(start.getTime()+2*60000);
  const fmt=d=>d.getHours().toString().padStart(2,'0')+':'+d.getMinutes().toString().padStart(2,'0');
  return {range:fmt(start)+' - '+fmt(end), wait:add};
}
games.forEach(g=>{
 const d=document.createElement('div');d.className='card';
 d.innerHTML=`<div style="width:100%;height:100%;background:linear-gradient(135deg,${g[2]},#0b0f1a);display:flex;align-items:center;justify-content:center;font-size:60px">${g[1]}</div><span class="badge">NOUVEAU</span><div class="card-content"><h3 style="font-size:12px;font-weight:800">${g[0]}</h3><p style="font-size:11px;color:#00e676">⚡ Signal prêt • ${getPlayTime().range}</p></div>`;
 d.onclick=()=>{
  const t=getPlayTime();const x=(Math.random()*6+1.5).toFixed(2);
  document.getElementById('mt').innerText=g[0];document.getElementById('ms').innerText='x'+x;document.getElementById('mc').innerText='x'+(x-0.5).toFixed(2);document.getElementById('mTime').innerText=t.range;document.getElementById('modal').classList.add('active');
 };grid.appendChild(d);
});
Telegram.WebApp.expand();
</script></body></html>
"""

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(HTML_APP.encode())

def run_server():
    port = int(os.environ.get("PORT", 10000))
    HTTPServer(("0.0.0.0", port), Handler).serve_forever()

threading.Thread(target=run_server, daemon=True).start()

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")
PROMO = "DINEROCFA225"
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://dinerocfa-aviator-bot.onrender.com")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = [[InlineKeyboardButton("📡 Signal", callback_data="signal")]]
    await update.message.reply_text("Que peut faire ce bot ?\nDinero CFA multi 1win games\n\nCliquez sur le bouton Signal en bas pour obtenir de signal", reply_markup=InlineKeyboardMarkup(kb))

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if q.data == "signal":
        kb = [[InlineKeyboardButton("➡️ Retour", callback_data="retour")]]
        await q.edit_message_text("Veuillez envoyer votre ID 1Win pour vérifier votre inscription.\n\nVotre ID 1Win se trouve dans votre profil 1Win.", reply_markup=InlineKeyboardMarkup(kb))
    elif q.data == "retour":
        kb = [[InlineKeyboardButton("📡 Signal", callback_data="signal")]]
        await q.edit_message_text("Que peut faire ce bot ?\nDinero CFA multi 1win games\n\nCliquez sur le bouton Signal en bas pour obtenir de signal", reply_markup=InlineKeyboardMarkup(kb))

async def check_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.text.strip().isdigit():
        await update.message.reply_text("Envoie ton ID 1Win (chiffres seulement) Ex: 385943982")
        return
    kb = [[InlineKeyboardButton("🎮 Accéder aux Prédictions", web_app=WebAppInfo(url=WEBAPP_URL))]]
    await update.message.reply_text(f"🏆 FÉLICITATIONS - ACCÈS VIP\n\nVous avez accès aux prédictions exclusives {PROMO} !\n\n👉 Cliquez ci-dessous pour accéder :", reply_markup=InlineKeyboardMarkup(kb))

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_id))
app.run_polling()
