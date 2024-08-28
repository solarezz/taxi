from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from db_handler.db_customers import Customers
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove, FSInputFile,
)
from keyboards.all_keyboards import *

start_router = Router()

customers = Customers()


class Form(StatesGroup):
    fullname = State()


@start_router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    cus = await customers.info(message.chat.id)
    if cus is None:
        await state.set_state(Form.fullname)
        await message.answer(
            'Здравствуйте! Чтобы начать, пожалуйста, укажите ваше имя и фамилию в формате "Иван Иванов"',
            reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer('Вы уже зарегистрированы!')


@start_router.message(Form.fullname)
async def process_fullname(message: Message, state: FSMContext):
    await customers.add_customer(fullname=message.text,
                                 telegram_user_id=message.chat.id)
    await message.answer('Теперь у вас есть возможность воспользоваться функционалом бота!',
                         reply_markup=menu_keyboard())
    await state.clear()

