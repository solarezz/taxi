from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import (
    Message, ReplyKeyboardRemove
)
from keyboards.all_keyboards import *
from db_handler.db_predrivers import PreDrivers

im_the_driver = Router()
pd = PreDrivers()


class Form(StatesGroup):
    driver_name = State()
    phone_number = State()
    experience = State()
    car = State()
    number_car = State()


@im_the_driver.message(F.text == '🚦 Я водитель')
async def im_driver(message: Message, state: FSMContext):
    await state.set_state(Form.driver_name)
    await message.answer('Здравствуйте, для отправки заявки требуется отправить ваше ФИО в формате "Иван Иванов":',
                         reply_markup=ReplyKeyboardRemove())


@im_the_driver.message(F.text, Form.driver_name)
async def process_fullname(message: Message, state: FSMContext):
    await state.update_data(driver_name=message.text)
    await message.answer(f'Отлично, {message.text}. Далее нам понадобится ваш номер в формате "+79999999999":')
    await state.set_state(Form.phone_number)


@im_the_driver.message(F.text, Form.phone_number)
async def process_number(message: Message, state: FSMContext):
    await state.update_data(phone_number=message.text)
    await message.answer('Теперь нам нужен Ваш стаж:')
    await state.set_state(Form.experience)


@im_the_driver.message(F.text, Form.experience)
async def process_experience(message: Message, state: FSMContext):
    await state.update_data(experience=message.text)
    await message.answer('Укажите ваше авто в формате "ВАЗ 2107":')
    await state.set_state(Form.car)


@im_the_driver.message(F.text, Form.car)
async def process_car(message: Message, state: FSMContext):
    await state.update_data(car=message.text)
    await message.answer('Отлично, укажите номер вашего авто в формате "А123АА 59":')
    await state.set_state(Form.number_car)


@im_the_driver.message(F.text, Form.number_car)
async def process_number_car(message: Message, state: FSMContext):
    await state.update_data(number_car=message.text)
    data = await state.get_data()
    await pd.driver_application(driver_name=data.get("driver_name"),
                                telegram_user_id=message.chat.id,
                                experience=data.get("experience"),
                                car=data.get("car"),
                                number_car=data.get("number_car"),
                                phone_number=data.get("phone_number"))
    await message.answer('Ваша заявка отправлена, ожидайте звонка!', reply_markup=menu_keyboard(message.chat.id))
    await state.clear()
