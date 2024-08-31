from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from filters.is_admin import IsAdmin
from db_handler.db_predrivers import PreDrivers

pd = PreDrivers()


def menu_keyboard(user_id):
    if not IsAdmin(user_id):
        menu = [
            [
                KeyboardButton(text='🚕 Сделать заказ'),
                KeyboardButton(text='👤 Профиль'),
                KeyboardButton(text='🚦 Я водитель')
            ]
        ]
        markup = ReplyKeyboardMarkup(keyboard=menu, resize_keyboard=True)
        return markup
    elif IsAdmin(user_id):
        menu = [
            [
                KeyboardButton(text='🚕 Сделать заказ'),
                KeyboardButton(text='👤 Профиль'),
                KeyboardButton(text='🚦 Я водитель'),
                KeyboardButton(text='📝 Проверить заявления')
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


def ex_predriver(phones):
    builder = ReplyKeyboardBuilder()
    for phone in phones:
        builder.add(KeyboardButton(text=str(phone)))
    builder.adjust(3)
    return builder.as_markup(resize_keyboard=True)
