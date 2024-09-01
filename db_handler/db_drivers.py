import aiosqlite
from db_handler.db_class import Database

db = Database()


class Drivers:
    async def info(self, telegram_user_id):
        async with aiosqlite.connect(db.db_file) as database:
            async with database.execute('SELECT * FROM drivers WHERE telegram_user_id=?',
                                        (telegram_user_id,)) as cur:
                info = await cur.fetchone()
                return info

    async def search(self):
        async with aiosqlite.connect(db.db_file) as database:
            async with database.execute('SELECT telegram_user_id FROM drivers WHERE status="Свободен"') as cur:
                drivers = await cur.fetchone()
                return drivers

    async def update_status(self, telegram_user_id):
        async with aiosqlite.connect(db.db_file) as database:
            await database.execute('UPDATE drivers SET status="Занят" WHERE telegram_user_id=?',
                                   (telegram_user_id,))
            await database.commit()

    async def update_photo(self, telegram_user_id, photo_directory):
        async with aiosqlite.connect(db.db_file) as database:
            await database.execute('UPDATE drivers SET photo = ? WHERE telegram_user_id = ?',
                                   (photo_directory,
                                    telegram_user_id))
            await database.commit()

