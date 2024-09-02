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

    async def phone_info(self):
        async with aiosqlite.connect(db.db_file) as database:
            async with database.execute('SELECT phone_number FROM pre_drivers') as cur:
                rows = await cur.fetchall()
                return [row[0] for row in rows]

    async def info(self, phone_number):
        async with aiosqlite.connect(db.db_file) as database:
            async with database.execute('SELECT * FROM pre_drivers WHERE phone_number=?', (phone_number,)) as cur:
                rows = await cur.fetchone()
                return rows

    async def delete(self, phone_number):
        async with aiosqlite.connect(db.db_file) as database:
            await database.execute("DELETE FROM pre_drivers WHERE phone_number = ?", (phone_number,))
            await database.commit()