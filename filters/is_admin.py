from decouple import config


class IsAdmin:
    def __init__(self, user_id):
        self.user_id = user_id

    async def checker(self):
        if self.user_id in config("ADMINS"):
            return True
        else:
            return False
