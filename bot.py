import telebot
from telebot import types
from flask import Flask, request
import os

# =========================
# 🔐 CONFIGURACIÓN DEL TOKEN
# =========================
TOKEN = os.getenv("BOT_TOKEN") or os.getenv("TOKEN")
if not TOKEN:
    raise Exception("❌ No se encontró el token del bot. Configura BOT_TOKEN o TOKEN en Render.")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# 🌍 Idioma por defecto
user_language = {}

# =========================
# 📜 FUNCIONES DE MENÚ
# =========================

def menu_principal(chat_id):
    """Muestra el menú principal con todas las opciones"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    botones = [
        "🐰 Canal VIP acompañada",
        "💖 Canal VIP sola",
        "🍒 Paquetes sola",
        "🍆 Paquetes acompañada",
        "⚡ Paquete flash",
        "💦 Videollamadas",
        "🎀 Promo fidelidad",
        "🌺 Video personalizado",
        "👑 Trato NOVIA VIRTUAL",
        "❤ Novia Virtual previa",
        "🍸 Conocerme más",
        "💳 Pagos 💸"
    ]
    for b in botones:
        markup.add(types.KeyboardButton(b))
    bot.send_message(chat_id, "🌸 *Elige una opción del menú:*", reply_markup=markup, parse_mode="Markdown")

# =========================
# 🧾 RESPUESTAS PERSONALIZADAS
# =========================

def responder_opcion(chat_id, opcion):
    """Responde según la opción elegida o emoji recibido"""
    respuestas = {
        "🐰": "🐰 *Canal VIP acompañada [adelantos]*\n💰 S/.110  |  $33",
        "💖": "💖 *Canal VIP sola [contenido completo]*\n💰 S/.99  |  $31",
        "🍒": "🍒 *Paquetes [videos y fotos] sola*\n💰 S/.59",
        "🍆": "🍆 *Paquetes acompañada [varía por video]*\n💰 +S/.120  |  $40",
        "⚡": "⚡ *Info de paquete flash*\n💰 S/.20  |  $10",
        "💦": "💦 *Videollamadas*\n💰 S/.70  |  $19",
        "🎀": "🎀 *Promo de fidelidad 3 meses*",
        "🌺": "🌺 *Video personalizado*",
        "👑": "👑 *Trato NOVIA VIRTUAL*\n💞 1 semana de fotos y videos explícitos + 2 videollamadas\n💰 S/.110  |  $33",
        "❤": "❤ *Se...ting / Novia Virtual previa*\n💞 Incluye 1 videollamada (30 min aprox)\n💰 S/.99  |  $31",
        "🍸": "🍸 *Para conocerme más*\n(Disponible solo para subs de Telegram u OF)",
        "💳": "💳 *Métodos de pago disponibles:*\n💸 Yape / Plin\n📲 Envía el monto al número **999 999 999** y adjunta tu comprobante 💌"
    }

    texto = respuestas.get(opcion)
    if texto:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("⬅️ Volver al menú principal")
        bot.send_message(chat_id, texto, reply_markup=markup, parse_mode="Markdown")
    else:
        bot.send_message(chat_id, "🤖 No entendí eso 💭, elige una opción o envíame un emoji 🍒")

# =========================
# 📨 MENSAJES ENTRANTES
# =========================

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    texto = message.text.lower().strip()

    # Saludos automáticos
    if texto in ["/start", "hola", "buenas", "hey", "hi"]:
        bot.send_message(message.chat.id, "👋 ¡Hola! Bienvenido a *Cherry Assistant* 💖")
        menu_principal(message.chat.id)
        return

    # Volver al menú
    if "volver" in texto or "menu" in texto:
        menu_principal(message.chat.id)
        return

    # Detección por texto o emoji
    emojis = ["🐰", "💖", "🍒", "🍆", "⚡", "💦", "🎀", "🌺", "👑", "❤", "🍸", "💳"]
    palabras = {
        "vip acompañada": "🐰",
        "vip sola": "💖",
        "paquete sola": "🍒",
        "paquete acompañada": "🍆",
        "flash": "⚡",
        "videollamada": "💦",
        "fidelidad": "🎀",
        "personalizado": "🌺",
        "novia virtual": "👑",
        "previa": "❤",
        "conocer": "🍸",
        "pago": "💳"
    }

    # Si el usuario manda un emoji válido
    for e in emojis:
        if e in texto:
            responder_opcion(message.chat.id, e)
            return

    # Si el usuario escribe palabras similares
    for palabra, emoji in palabras.items():
        if palabra in texto:
            responder_opcion(message.chat.id, emoji)
            return

    # Si no se reconoce
    bot.send_message(message.chat.id, "🤖 No entendí eso 💭, elige una opción del menú o envíame un emoji 🍒")

# =========================
# 🌐 WEBHOOK PARA RENDER
# =========================

@app.route('/')
def index():
    return "🍒 Cherry Assistant activo 💖"

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    return "ok", 200

# =========================
# 🚀 EJECUCIÓN PRINCIPAL
# =========================

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/{TOKEN}")
    app.run(host="0.0.0.0", port=10000)
