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
