import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import os

TOKEN = os.getenv("8717809394:AAFP5U65HBRkDdWF8O77S2pBNsETG87EIUU")
OWNER_ID = 8409147278

bot = telebot.TeleBot(8717809394:AAFP5U65HBRkDdWF8O77S2pBNsETG87EIUU)

user_data = {}

# Клавиатуры
phone_keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
phone_keyboard.add(KeyboardButton("📱 Отправить номер", request_contact=True))

window_keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
window_keyboard.add("Пластиковые", "Деревянные", "Алюминиевые", "Энергосберегающие")

# Обработчики команд
@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    user_data[chat_id] = {}
    bot.send_message(chat_id, "🪟 Окна Большой Страны КБР\n\nКак вас зовут?")
    bot.register_next_step_handler(message, get_name)

def get_name(message):
    chat_id = message.chat.id
    user_data[chat_id]['name'] = message.text
    bot.send_message(chat_id, "📞 Ваш номер телефона:", reply_markup=phone_keyboard)
    bot.register_next_step_handler(message, get_phone)

def get_phone(message):
    chat_id = message.chat.id
    if message.contact:
        phone = message.contact.phone_number
    else:
        phone = message.text
    user_data[chat_id]['phone'] = phone
    bot.send_message(chat_id, "📍 Ваш адрес (город, улица, дом):", reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(message, get_address)

def get_address(message):
    chat_id = message.chat.id
    user_data[chat_id]['address'] = message.text
    bot.send_message(chat_id, "🪟 Тип окон:", reply_markup=window_keyboard)
    bot.register_next_step_handler(message, get_window_type)

def get_window_type(message):
    chat_id = message.chat.id
    user_data[chat_id]['window_type'] = message.text
    bot.send_message(chat_id, "📅 Желаемая дата замера:", reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(message, get_date)

def get_date(message):
    chat_id = message.chat.id
    user_data[chat_id]['date'] = message.text
    bot.send_message(chat_id, "📝 Пожелания (или «Нет»):")
    bot.register_next_step_handler(message, get_comment)

def get_comment(message):
    chat_id = message.chat.id
    comment = message.text
    if comment.lower() == "нет":
        comment = "—"
    user_data[chat_id]['comment'] = comment
    data = user_data[chat_id]
    order_text = (
        f"🪟 НОВЫЙ ЗАКАЗ\n\n"
        f"Имя: {data['name']}\n"
        f"Телефон: {data['phone']}\n"
        f"Адрес: {data['address']}\n"
        f"Тип окон: {data['window_type']}\n"
        f"Дата замера: {data['date']}\n"
        f"Комментарий: {data['comment']}\n"
        f"Клиент: @{message.from_user.username or 'нет'} (ID: {chat_id})"
    )
    bot.send_message(OWNER_ID, order_text)
    bot.send_message(chat_id, "✅ Заявка принята! Специалист свяжется с вами.\n\n/start – новый заказ", reply_markup=ReplyKeyboardRemove())
    del user_data[chat_id]

@bot.message_handler(func=lambda message: True)
def unknown(message):
    bot.send_message(message.chat.id, "Нажмите /start, чтобы оформить заказ.")

if name == "main":
    print("Бот запущен")
    bot.infinity_polling()
