from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import (
    Message, ReplyKeyboardRemove
)

from create_bot import bot
from filters.is_admin import IsAdmin
from keyboards.all_keyboards import ex_predriver, yes_or_no, menu_keyboard
from db_handler.db_predrivers import PreDrivers

ex = Router()
pd = PreDrivers()


class Form(StatesGroup):
    choice_exam = State()
    choices = State()


@ex.message(F.text == "📝 Проверить заявления")
async def examination(message: Message, state: FSMContext):
    phones = await pd.phone_info()
    if IsAdmin(message.chat.id):
        ReplyKeyboardRemove()
        if phones:
            await message.answer("Выберите заявление:", reply_markup=ex_predriver(phones))
            await state.set_state(Form.choice_exam)
        else:
            await message.answer("Заявлений нет!", reply_markup=menu_keyboard(message.chat.id))
            await state.clear()


@ex.message(F.text, Form.choice_exam)
async def if_phone(message: Message, state: FSMContext):
    phones = await pd.phone_info()
    phone = message.text
    if phone in phones:
        pred = await pd.info(phone)
        await state.update_data(phone=phone)
        await state.set_state(Form.choices)
        await message.answer(f"""
Информация по заявлению -
Имя: {pred[1]}
Стаж: {pred[3]}
Машина: {pred[4]}
Номер машины: {pred[5]}""",
                             reply_markup=yes_or_no())


@ex.message(F.text, Form.choices)
async def choice_process(message: Message, state: FSMContext):
    await state.update_data(msg=message.text)
    data = await state.get_data()
    info = await pd.info(data.get("phone"))

    print(f"---Message: {data.get('msg')}, Info: {info}---")

    if data.get("msg") == "🟢 Подходит":
        await message.answer('Отправлено пользователю!', reply_markup=menu_keyboard(message.chat.id))
        try:
            await bot.send_message(info[2], "Вы нам подходите, ожидайте звонка!")
            await pd.delete(phone_number=data.get("phone"))
        except Exception as e:
            print(f"Error sending message: {e}")

    elif data.get("msg") == "🔴 Не подходит":
        await message.answer('Отправлено пользователю!', reply_markup=menu_keyboard(message.chat.id))
        try:
            await bot.send_message(info[2], "Вы нам не подходите!")
            await pd.delete(phone_number=data.get("phone"))
        except Exception as e:
            print(f"Error sending message: {e}")
    await state.clear()

