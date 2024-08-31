import asyncio
from create_bot import bot, dp
from handlers import start, profile, change_avatar, im_the_driver, examination


# from work_time.time_func import send_time_msg

async def main():
    dp.include_router(router=start.start_router)
    dp.include_router(router=profile.profile_router)
    dp.include_router(router=change_avatar.change_photo)
    dp.include_router(router=im_the_driver.im_the_driver)
    dp.include_router(router=examination.ex)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
