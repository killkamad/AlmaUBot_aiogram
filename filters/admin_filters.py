from aiogram.dispatcher.filters import BoundFilter
from aiogram import types
from utils import db_api as db


class AdminFilter(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin):
        self.is_admin = is_admin

    async def check(self, message: types.Message):
        admin = await db.check_role_by_id(message.chat.id, 'admin') == 'admin'
        return admin


class AdminFilterCallBack(BoundFilter):
    key = 'is_admin_c'

    def __init__(self, is_admin_c):
        self.is_admin_c = is_admin_c

    async def check(self, call: types.CallbackQuery):
        admin = await db.check_role_by_id(call.message.chat.id, 'admin') == 'admin'
        return admin


class LibraryAdminFilter(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin):
        self.is_admin = is_admin

    async def check(self, message: types.Message):
        admin = await db.check_role_by_id(message.chat.id, 'admin') == 'admin'
        return admin
