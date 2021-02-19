from aiogram import Dispatcher
from .admin_filters import AdminFilter, AdminFilterCallBack


def setup(dp: Dispatcher):
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(AdminFilterCallBack)
