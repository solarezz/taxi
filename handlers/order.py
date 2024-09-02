from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, FSInputFile, ReplyKeyboardRemove
from db_handler.db_drivers import Drivers
from db_handler.db_customers import Customers
from create_bot import bot
from keyboards.all_keyboards import menu_keyboard

dr = Drivers()
customers = Customers()

orders = Router()


class Form(StatesGroup):
    my_street = State()
    where = State()




@orders.message(F.text == '🚕 Сделать заказ')
async def order(message: Message, state: FSMContext):
    await state.set_state(Form.my_street)
    await message.delete()
    ReplyKeyboardRemove()
    msg = await bot.send_message(message.chat.id, 'Напишите откуда вас забрать:')
    await state.update_data(msg=msg.message_id)


@orders.message(F.text, Form.my_street)
async def my_street_process(message: Message, state: FSMContext):
    await state.update_data(my_street=message.text)
    await state.set_state(Form.where)
    await message.delete()
    data = await state.get_data()
    msg = await bot.edit_message_text(text='Напиши куда вас отвезти:',
                                    chat_id=message.chat.id,
                                    message_id=data.get("msg"))
    await state.update_data(msg=msg.message_id)



@orders.message(F.text, Form.where)
async def where_process(message: Message, state: FSMContext):
    await state.update_data(where=message.text)
    await message.delete()
    data = await state.get_data()
    msg = await bot.edit_message_text(text='Ожидайте, идёт поиск водителя...',
                                chat_id=message.chat.id,
                                message_id=data.get("msg"))
    await state.update_data(msg=msg.message_id)
    cus = await customers.info(telegram_user_id=message.chat.id)
    drivers = await dr.search()
    if drivers:
        for driver in drivers:
            data = await state.get_data()
            await bot.send_photo(driver, photo=FSInputFile(cus[4]), caption=f"""
    Заказ -
    Имя: {cus[1]}
    Откуда забрать: {data.get("my_street")}
    Куда ехать: {data.get("where")}
            """, reply_markup=menu_keyboard(message.chat.id))
            info_dr = await dr.info(driver)
            await message.answer_photo(photo=FSInputFile(info_dr[7]), caption=f"""
    За вами приедет:
    Имя: {info_dr[1]}
    Номер телефона: {info_dr[9]}
    Машина: {info_dr[4]}
    Номер машины: {info_dr[5]}
    Стаж: {info_dr[3]}"""
                                       , reply_markup=menu_keyboard(message.chat.id))
            await dr.update_status(driver)
            break
    else:
        await message.answer('Все водители заняты, попробуйте позже!')


"""
cus = await customers.info(telegram_user_id=message.chat.id)
    await message.answer('Ищем водителя...')
    drivers = await dr.search()
    for driver in drivers:
        bot.send_photo(driver, photo=FSInputFile(cus[4]), caption=f'Имя:{cus[1]}\nКуда: ')
"""
