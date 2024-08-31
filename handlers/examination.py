from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import (
    Message, ReplyKeyboardRemove
)

from filters.is_admin import IsAdmin
from keyboards.all_keyboards import ex_predriver
from db_handler.db_predrivers import PreDrivers

ex = Router()
pd = PreDrivers()


class Form(StatesGroup):
    choice = State()


@ex.message(F.text == "📝 Проверить заявления")
async def examination(message: Message, state: FSMContext):
    phones = await pd.info()
    print(phones)
    if IsAdmin(message.chat.id):
        ReplyKeyboardRemove()
        await message.answer("Выберите заявление:", reply_markup=ex_predriver(phones))
