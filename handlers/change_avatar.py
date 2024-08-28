from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    Message,
    CallbackQuery
)
from db_handler.db_customers import Customers
from db_handler.db_drivers import Drivers

change_photo = Router()
drivers = Drivers()
customers = Customers()


class Form(StatesGroup):
    wait_photo = State()


@change_photo.callback_query(F.data == 'change_photo')
async def change(call: CallbackQuery, state: FSMContext):
    await state.set_state(Form.wait_photo)
    await call.message.answer('Отправьте Вашу фотографию, чтобы обновить своё фото!')


@change_photo.message(F.photo, Form.wait_photo)
async def take_photo(message: Message, state: FSMContext):
    dr = await drivers.info(message.chat.id)
    cus = await customers.info(message.chat.id)
    if dr:
        await state.clear()
    elif cus:
        await message.bot.download(file=message.photo[-1].file_id, destination=f'avatars/{message.chat.id}.png')
        await customers.update_photo(telegram_user_id=message.chat.id,
                                     photo_directory=f'avatars/{message.chat.id}.png')
        await message.answer('Ваше фото обновлено!')
        await state.clear()
    else:
        await message.answer('Вас нет в базе данных! Введите команду - /start')
        await state.clear()
