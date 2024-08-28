from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup


def menu_keyboard():
    menu = [
        [
            KeyboardButton(text='🚕 Сделать заказ'),
            KeyboardButton(text='👤 Профиль'),
            KeyboardButton(text='🚦 Я водитель')
        ]
    ]
    markup = ReplyKeyboardMarkup(keyboard=menu, resize_keyboard=True)
    return markup

def change_avatar():
    change = [
        [
            InlineKeyboardButton(text="Сменить фото", callback_data='change_photo')
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=change)
    return keyboard
