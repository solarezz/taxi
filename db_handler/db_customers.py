import aiosqlite
from db_handler.db_class import Database

db = Database()


class Customers:
    async def add_customer(self, fullname, telegram_user_id):
        async with aiosqlite.connect(db.db_file) as database:
            await database.execute('INSERT OR IGNORE INTO customers (fullname, telegram_user_id) VALUES (?, ?)',
                                   (fullname,
                                    telegram_user_id))
            await database.commit()

    async def info(self, telegram_user_id):
        async with aiosqlite.connect(db.db_file) as database:
            async with database.execute('SELECT * FROM customers WHERE telegram_user_id=?',
                                        (telegram_user_id,)) as cur:
                info = await cur.fetchone()
                return info

    async def update_photo(self, telegram_user_id, photo_directory):
        async with aiosqlite.connect(db.db_file) as database:
            await database.execute('UPDATE customers SET photo = ? WHERE telegram_user_id = ?',
                                   (photo_directory,
                                    telegram_user_id))
            await database.commit()