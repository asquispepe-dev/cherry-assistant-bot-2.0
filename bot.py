import telebot
from telebot import types
from flask import Flask, request
import os

# TOKEN del bot (Render -> Environment variables -> BOT_TOKEN)
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# ======================
# 🌍 CONFIGURACIONES
# ======================
user_state = {}

# ======================
# 💬 MENSAJE DE INICIO
# ======================
def send_welcome(message):
    text = (
        "💖 Hola\n"
        "Aquí puedes ver toda mi info y elegir lo que desees 💋"
    )

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [
        "🐰 Canal VIP acompañada",
        "💖 Canal VIP sola",
        "🍒 Paquetes sola",
        "🍆 Paquetes acompañada",
        "💦 Videollamadas",
        "💸 Pagos"
    ]
    markup.add(*buttons)

    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="Markdown")

# ======================
# 🏠 VOLVER AL MENÚ
# ======================
def back_to_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [
        "🐰 Canal VIP acompañada",
        "💖 Canal VIP sola",
        "🍒 Paquetes sola",
        "🍆 Paquetes acompañada",
        "💦 Videollamadas",
        "💸 Pagos"
    ]
    markup.add(*buttons)
    bot.send_message(message.chat.id, "🏠 Volviste al menú principal 💞", reply_markup=markup)

# ======================
# 📜 RESPUESTAS DE OPCIONES
# ======================
def handle_option(message, option):
    texts = {
        "🐰 Canal VIP acompañada": """🐰 Canal VIP acompañada [adelantos] S/.150 $45

Descubre mis momentos más *intensos y reales* 💖 Encuentros con mi pareja grabados en diferentes spots … en mi mood más apasionado 💞

📹 Contenido:
🎀 Clips +1min, sin censura ni marcas de agua 
🎀 Grabados en HD, con buena iluminación
🎀 Escenas acompañadas con todo el detalle explícito 💋

💎 Incluye:
🎀 Acceso al canal de adelantos “Acompañada”
🎬 +5 adelantos 

💸 Suscripción:
⭐ 1 mes: S/.150 (≈ $45)
⭐ 2 meses: S/.220 (≈ $65)""",

        "💖 Canal VIP sola": """💖⭐ Canal VIP Sola ⭐💖
Aquí te muestro mi día a día pero en mood horny 😈 en lencería | ropa casual y más. 
Me vas a ver y escuchar dándome placer 💦🔥 bañándome y jugando conmigo en diferentes situaciones. 
Fotos y videos sin censura ni marcas de agua…

🌺 Contenido explícito, cutie y muy íntimo:

💸 Suscripción:
⭐ 1 mes: S/.99 (≈ $33)
⭐ 2 meses: S/.160 (≈ $49)""",

        "🍒 Paquetes sola": """⭐ Paquetes SOLA ⭐🍒 @bycherryyy

🎀⚡ 4 videos: 1min cada uno [ acariciándome, másxxx, con juguetes o dedos 😳 mostrando rostro y 🍑 ]
💸 S/.99 (≈ $33)

💖 Métodos de pago:
Transferencia bancaria | Western Union | PayPal | A través de OF | Yape / Plin 💸""",

        "🍆 Paquetes acompañada": """🌟 Paquetes Acompañada @bycheryyy 🍒🍆

Momentos intensos, reales y sin filtros 💋 Escenas completas con mi pareja grabadas en distintos spots: carretera, playa, etc. Cada video con una energía única y muy natural 🔥

🎬 Detalles del contenido:
🍒 Videos acompañada (3–16 minutos)
🍒 Grabados en HD o 4K
🍒 Buena iluminación y audio real

💎 Precios:
💖 Desde S/.100 hasta S/.160 (≈ $30–$55)
💖 Varía según duración e intensidad

💸 Métodos de pago:
Yape | Plin | Transferencia | Western Union | PayPal | A través de OF""",

        "💦 Videollamadas": """💦 Videollamada 🎀💖 *mood novia virtual* 💕 
En lencería | conversación 🔥 usando mis dedos o juguetes 🕹 en las poses que elijas 💖

⌛ Duración: 15–30 min

📆 Reserva:
🎀 Se confirma con 50% de anticipación.
Garantiza tu espacio ya que ambos debemos tener tiempo y privacidad 🎥💋

💎 Precios:
S/.70 o $20 | +S/.20 o $5 con juguetes 🧸🕹

💸 Métodos de pago:
Transferencia | Western Union | PayPal | OF | Yape / Plin 💖"""
    }

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🏠 Volver al menú principal")
    bot.send_message(message.chat.id, texts.get(option, "💖 Opción no encontrada."), reply_markup=markup, parse_mode="Markdown")

# ======================
# 💳 PAGOS
# ======================
def handle_payments(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("💸 Pagar por Yape / Plin", callback_data="pay_yape")
    markup.add(btn1)
    text = (
        "💳 *Métodos de pago disponibles:*\n\n"
        "Selecciona una opción para continuar con tu pago 💖"
    )
    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="Markdown")

# ======================
# 🎯 CALLBACKS
# ======================
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "pay_yape":
        bot.answer_callback_query(call.id)
        bot.send_message(
            call.message.chat.id,
            "💸 *Pago Yape / Plin:*\n\n"
            "Envía el monto al número **999 999 999** 📲\n"
            "Adjunta tu comprobante aquí 💌 y se validará tu pago.\n\n"
            "Una vez confirmado, recibirás tu acceso o contenido correspondiente 💖",
            parse_mode="Markdown"
        )

# ======================
# 📥 MENSAJES DE USUARIO
# ======================
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text.strip().lower()

    if text in ["hola", "hi", "buenas", "/start"]:
        send_welcome(message)
    elif text in ["🏠 volver al menú principal", "volver", "menu", "menú"]:
        back_to_menu(message)
    elif any(kw in text for kw in ["pago", "pagar", "plin", "yape"]):
        handle_payments(message)
    elif any(kw in text for kw in ["canal acompañada", "🐰"]):
        handle_option(message, "🐰 Canal VIP acompañada")
    elif any(kw in text for kw in ["canal sola", "💖"]):
        handle_option(message, "💖 Canal VIP sola")
    elif any(kw in text for kw in ["paquete sola", "🍒"]):
        handle_option(message, "🍒 Paquetes sola")
    elif any(kw in text for kw in ["paquete acompañada", "🍆"]):
        handle_option(message, "🍆 Paquetes acompañada")
    elif any(kw in text for kw in ["videollamada", "💦"]):
        handle_option(message, "💦 Videollamadas")
    else:
        bot.send_message(
            message.chat.id,
            "💋 No entendí eso, por favor elige una opción del menú 💖",
            parse_mode="Markdown"
        )

# ======================
# 🌐 WEBHOOK PARA RENDER
# ======================
@app.route('/')
def index():
    return "Bot activo 💋"

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    return "ok", 200

# ======================
# 🚀 EJECUCIÓN PRINCIPAL
# ======================
if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/{TOKEN}")
    app.run(host="0.0.0.0", port=10000)
