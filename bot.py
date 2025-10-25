import telebot
from telebot import types
from flask import Flask, request
import os

# 🔐 TOKEN de tu bot (se configura en Render como variable de entorno)
TOKEN = os.getenv("8350135404:AAFvClHUwuMMy2yReawp7qml1tdjzfZ3cDo")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# 🌍 Idioma por defecto de cada usuario
user_language = {}

# ======================
# 🧠 FUNCIONES PRINCIPALES
# ======================

def send_welcome(message):
    """Mensaje de bienvenida con botones principales"""
    lang = user_language.get(message.chat.id, "es")
    
    if lang == "es":
        text = (
            "👋 ¡Hola! Bienvenido a *Cherry Assistant* 💖\n\n"
            "Soy tu asistente virtual, aquí para ayudarte con toda la información de nuestros servicios.\n"
            "Por favor, elige una opción del menú:"
        )
        buttons = ["ℹ️ Información", "🎁 Promociones", "💬 Atención al cliente", "💳 Pagos", "🌎 Cambiar idioma"]
    else:
        text = (
            "👋 Hello! Welcome to *Cherry Assistant* 💖\n\n"
            "I’m your virtual assistant, ready to help you.\n"
            "Please choose an option:"
        )
        buttons = ["ℹ️ Information", "🎁 Promotions", "💬 Support", "💳 Payments", "🌎 Change language"]

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for b in buttons:
        markup.add(b)
    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="Markdown")


# ======================
# 📜 RESPUESTAS DEL MENÚ PRINCIPAL
# ======================

def handle_info(message):
    """📍 AQUÍ PEGAS TUS TEXTOS DE INFORMACIÓN PRINCIPAL"""
    lang = user_language.get(message.chat.id, "es")
    if lang == "es":
        text = (
            "📚 *Información general de nuestros servicios:*\n\n"
            "➡️ Aquí puedes pegar todo el texto que me enviaste sobre tus planes y paquetes.\n"
            "Por ejemplo:\n"
            "🐰 Canal VIP acompañada...\n"
            "💖 Canal VIP sola...\n"
            "🍒 Paquetes sola...\n"
            "🍆 Paquetes acompañada...\n"
            "💦 Videollamadas...\n"
            "\n💡 (Solo copia y pega tu información aquí dentro de este mensaje)"
        )
    else:
        text = "📚 *General information about our services.*\nYou can paste your English version here."
    bot.send_message(message.chat.id, text, parse_mode="Markdown")


def handle_promotions(message):
    """📍 AQUÍ PEGAS LAS PROMOCIONES"""
    lang = user_language.get(message.chat.id, "es")
    if lang == "es":
        text = (
            "🎁 *Promociones activas:*\n\n"
            "💖 Puedes pegar aquí tus promos actuales o futuras.\n"
            "Por ejemplo:\n"
            "🎀 Promo de fidelidad 3 meses\n"
            "🌸 Descuento especial por referidos\n"
        )
    else:
        text = "🎁 *Active promotions:* Paste here your English version."
    bot.send_message(message.chat.id, text, parse_mode="Markdown")


def handle_support(message):
    """📍 SECCIÓN DE ATENCIÓN AL CLIENTE"""
    lang = user_language.get(message.chat.id, "es")
    if lang == "es":
        text = (
            "💬 *Atención al cliente:*\n"
            "Por favor escribe tu consulta y te ayudaremos lo antes posible 💌"
        )
    else:
        text = "💬 *Customer Support:*\nPlease write your question and we’ll get back to you soon 💌"
    bot.send_message(message.chat.id, text, parse_mode="Markdown")


def handle_payments(message):
    """📍 SECCIÓN DE PAGOS"""
    lang = user_language.get(message.chat.id, "es")
    if lang == "es":
        markup = types.InlineKeyboardMarkup()
        
        # 💳 BOTONES DE OPCIONES DE PAGO
        btn1 = types.InlineKeyboardButton("💸 Pagar por Yape / Plin", callback_data="pay_yape")
        markup.add(btn1)

        text = (
            "💳 *Métodos de pago disponibles:*\n\n"
            "Selecciona una opción para continuar con tu pago 💖"
        )
    else:
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton("💸 Pay via Yape / Plin", callback_data="pay_yape")
        markup.add(btn1)

        text = (
            "💳 *Available payment methods:*\n\n"
            "Choose a payment method 💖"
        )

    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="Markdown")


def change_language(message):
    """📍 CAMBIO DE IDIOMA"""
    lang = user_language.get(message.chat.id, "es")
    if lang == "es":
        user_language[message.chat.id] = "en"
        bot.send_message(message.chat.id, "🌎 Idioma cambiado a *Inglés* 🇬🇧", parse_mode="Markdown")
    else:
        user_language[message.chat.id] = "es"
        bot.send_message(message.chat.id, "🌎 Language changed to *Spanish* 🇪🇸", parse_mode="Markdown")
    send_welcome(message)


# ======================
# 🎯 CALLBACKS DE BOTONES INLINE
# ======================

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    """📍 AQUÍ SE MANEJAN LOS BOTONES (por ejemplo pagos)"""
    if call.data == "pay_yape":
        bot.answer_callback_query(call.id)
        bot.send_message(
            call.message.chat.id,
            "💸 *Pago Yape / Plin:*\n\n"
            "Envía el monto correspondiente al número **999 999 999** 📲\n"
            "Luego adjunta tu comprobante aquí 💌\n\n"
            "Tras confirmar tu pago, recibirás automáticamente tu acceso:\n"
            "👉 [Aquí irá tu link o texto de acceso personalizado]\n"
            "\n💡 (Puedes reemplazar este texto con el enlace real o el contenido del servicio pagado)",
            parse_mode="Markdown"
        )


# ======================
# 📥 RECEPCIÓN DE MENSAJES
# ======================

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text.lower()

    if text in ["/start", "hola", "buenas", "hey", "hi", "hello"]:
        send_welcome(message)
    elif "información" in text or "information" in text:
        handle_info(message)
    elif "promociones" in text or "promotions" in text:
        handle_promotions(message)
    elif "cliente" in text or "support" in text:
        handle_support(message)
    elif "pago" in text or "payments" in text:
        handle_payments(message)
    elif "idioma" in text or "language" in text:
        change_language(message)
    else:
        bot.send_message(
            message.chat.id,
            "🤖 No entendí eso, por favor selecciona una opción del menú principal.",
            parse_mode="Markdown"
        )


# ======================
# 🌐 WEBHOOK PARA RENDER
# ======================

@app.route('/')
def index():
    return "Cherry Assistant activo 💖"

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
