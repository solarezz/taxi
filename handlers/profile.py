from aiogram import Router, F
from aiogram.types import (
    Message,
    FSInputFile
)
from db_handler.db_drivers import Drivers
from db_handler.db_customers import Customers
from keyboards.all_keyboards import *


profile_router = Router()
drivers = Drivers()
customers = Customers()


@profile_router.message(F.text == '👤 Профиль')
async def profile(message: Message):
    cus = await customers.info(message.chat.id)
    print(cus)
    if cus:
        await message.answer_photo(photo=FSInputFile(cus[4]), caption=f"""
—

Профиль:

- Имя: {cus[1]}
- Оценка: {cus[3]}

—
        """, reply_markup=change_avatar())
