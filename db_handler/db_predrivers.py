import aiosqlite
from db_handler.db_class import Database

db = Database()


class PreDrivers:
    async def driver_application(self, driver_name, telegram_user_id, experience, car, number_car, phone_number):
        async with aiosqlite.connect(db.db_file) as database:
            await database.execute(
                'INSERT OR IGNORE INTO pre_drivers (driver_name, telegram_user_id, experience, car, number_car, phone_number) VALUES (?, ?, ?, ?, ?, ?)',
                (driver_name,
                 telegram_user_id,
                 experience,
                 car,
                 number_car,
                 phone_number))
            await database.commit()
