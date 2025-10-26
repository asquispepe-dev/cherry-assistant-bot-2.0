import telebot
from telebot import types
from flask import Flask, request
import os
import random

# ======================
# 🔐 CONFIGURACIÓN DEL BOT
# ======================
TOKEN = os.getenv("BOT_TOKEN") or os.getenv("TOKEN")
if not TOKEN:
    raise Exception("❌ Bot token no encontrado. Configúralo en Render como BOT_TOKEN o TOKEN")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# 🌍 Idioma por defecto de cada usuario
user_language = {}

# ======================
# 🧠 FUNCIÓN DE BIENVENIDA
# ======================
def send_welcome(message):
    lang = user_language.get(message.chat.id, "es")

    if lang == "es":
        text = (
            "👋 ¡Hola! Bienvenido a *Cherry Assistant* 💖\n\n"
            "Soy tu asistente virtual automatizado, lista para ayudarte con toda la información de nuestros servicios.\n"
            "Selecciona una opción del menú o envíame un emoji correspondiente 👇"
        )
        buttons = [
            ("ℹ️ Información", "ℹ️"),
            ("🎁 Promociones", "🎁"),
            ("💬 Atención al cliente", "💬"),
            ("💳 Pagos", "💳"),
            ("🌎 Cambiar idioma", "🌎")
        ]
    else:
        text = (
            "👋 Hello! Welcome to *Cherry Assistant* 💖\n\n"
            "I’m your virtual assistant, ready to help you with any info about our services.\n"
            "Select an option or send an emoji 👇"
        )
        buttons = [
            ("ℹ️ Information", "ℹ️"),
            ("🎁 Promotions", "🎁"),
            ("💬 Support", "💬"),
            ("💳 Payments", "💳"),
            ("🌎 Change language", "🌎")
        ]

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for label, emoji in buttons:
        markup.add(f"{emoji} {label}")

    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="Markdown")

# ======================
# 📜 FUNCIONES DE RESPUESTA
# ======================
def handle_info(message):
    lang = user_language.get(message.chat.id, "es")
    emoji = random.choice(["📖", "✨", "💡"])
    if lang == "es":
        text = (
            f"{emoji} *Información general:*\n\n"
            "Aquí puedes colocar toda la descripción de tus servicios.\n"
            "Ejemplo:\n"
            "🐰 Canal VIP acompañada...\n"
            "🍒 Paquetes sola...\n"
            "💦 Videollamadas...\n"
        )
    else:
        text = f"{emoji} *General Information:* Paste your English version here."
    bot.send_message(message.chat.id, text, parse_mode="Markdown")


def handle_promotions(message):
    lang = user_language.get(message.chat.id, "es")
    emoji = random.choice(["🎉", "💖", "🛍️"])
    if lang == "es":
        text = (
            f"{emoji} *Promociones activas:*\n\n"
            "💖 Aquí puedes detallar tus promociones o descuentos actuales.\n"
        )
    else:
        text = f"{emoji} *Active promotions:* Paste your English version here."
    bot.send_message(message.chat.id, text, parse_mode="Markdown")


def handle_support(message):
    lang = user_language.get(message.chat.id, "es")
    emoji = random.choice(["💬", "🙋‍♀️", "📩"])
    if lang == "es":
        text = (
            f"{emoji} *Atención al cliente:*\n"
            "Por favor, escribe tu consulta y te ayudaremos lo antes posible 💌"
        )
    else:
        text = f"{emoji} *Customer Support:* Write your question and we’ll get back soon 💌"
    bot.send_message(message.chat.id, text, parse_mode="Markdown")


def handle_payments(message):
    lang = user_language.get(message.chat.id, "es")
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("💸 Yape / Plin", callback_data="pay_yape")
    markup.add(btn1)

    emoji = random.choice(["💳", "💸", "🪙"])
    if lang == "es":
        text = (
            f"{emoji} *Métodos de pago disponibles:*\n\n"
            "Selecciona una opción para continuar con tu pago 💖"
        )
    else:
        text = f"{emoji} *Available payment methods:* Choose one to continue 💖"

    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="Markdown")


def change_language(message):
    lang = user_language.get(message.chat.id, "es")
    if lang == "es":
        user_language[message.chat.id] = "en"
        bot.send_message(message.chat.id, "🌎 Idioma cambiado a *Inglés* 🇬🇧", parse_mode="Markdown")
    else:
        user_language[message.chat.id] = "es"
        bot.send_message(message.chat.id, "🌎 Language changed to *Spanish* 🇪🇸", parse_mode="Markdown")
    send_welcome(message)

# ======================
# 🎯 CALLBACK DE PAGOS
# ======================
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "pay_yape":
        bot.answer_callback_query(call.id)
        bot.send_message(
            call.message.chat.id,
            "💸 *Pago Yape / Plin:*\n\n"
            "Envía el monto correspondiente al número **999 999 999** 📲\n"
            "Luego adjunta tu comprobante aquí 💌\n\n"
            "Tras confirmar tu pago, recibirás tu acceso:\n"
            "👉 [Aquí va tu link o texto personalizado]",
            parse_mode="Markdown"
        )

# ======================
# 🤖 DETECCIÓN DE MENSAJES Y RESPUESTAS NATURALES
# ======================
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text.lower()

    # Reacciones naturales (según lo que diga el usuario)
    respuestas_alegres = ["😄", "💖", "✨", "😊", "🥰"]
    respuestas_duda = ["🤔", "❓", "🙃", "💭"]
    respuestas_gracias = ["💝", "💫", "🙌", "❤️"]

    if "gracias" in text:
        bot.send_message(message.chat.id, f"¡De nada! {random.choice(respuestas_gracias)}", parse_mode="Markdown")
        return
    if "bot" in text:
        bot.send_message(message.chat.id, "🤖 ¡Sí! Soy *Cherry Assistant*, tu asistente virtual 💕", parse_mode="Markdown")
        return
    if any(word in text for word in ["hola", "hey", "hello", "buenas"]):
        bot.send_message(message.chat.id, f"¡Hola! {random.choice(respuestas_alegres)}", parse_mode="Markdown")
        send_welcome(message)
        return

    # Emojis y comandos del menú
    if "ℹ️" in text or "info" in text or "información" in text:
        handle_info(message)
    elif "🎁" in text or "promo" in text or "promoción" in text:
        handle_promotions(message)
    elif "💬" in text or "cliente" in text or "soporte" in text or "ayuda" in text:
        handle_support(message)
    elif "💳" in text or "pago" in text or "pay" in text:
        handle_payments(message)
    elif "🌎" in text or "idioma" in text or "language" in text:
        change_language(message)
    elif text in ["/start"]:
        send_welcome(message)
    else:
        bot.send_message(
            message.chat.id,
            f"🤖 No entendí eso {random.choice(respuestas_duda)} pero puedes elegir una opción del menú o enviarme un emoji 💬",
            parse_mode="Markdown"
        )

# ======================
# 🌐 WEBHOOK PARA RENDER
# ======================
@app.route('/')
def index():
    return "Cherry Assistant v4.0 activo 💖"

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
