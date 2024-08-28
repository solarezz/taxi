import aiosqlite


class Database:
    def __init__(self, db_file='database.db'):
        self.db_file = db_file
