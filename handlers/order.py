from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from db_handler.db_drivers import Drivers
from db_handler.db_customers import Customers
from create_bot import bot

dr = Drivers
customers = Customers

order = Router()

@order.message(F.text == '🚕 Сделать заказ')
async def order(message: Message):
    cus = await customers.info(message.chat.id)
    await message.answer('Ищем водителя...')
    drivers = await dr.search()
    for driver in drivers:
        bot.send_photo(driver, photo=FSInputFile(cus[4]), caption=f'Имя:{cus[1]}\nКуда: ')