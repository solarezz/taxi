import asyncio
from create_bot import bot, dp
from handlers.start import start_router


# from work_time.time_func import send_time_msg

async def main():
    dp.include_router(start_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
