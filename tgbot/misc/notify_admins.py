import logging

from aiogram import Dispatcher


async def notify_admins(dp: Dispatcher):
    admins = dp.bot.get('config').tg_bot.admin_ids
    for admin in admins:
        try:
            await dp.bot.send_message(admin, 'Бот запущен!')
        except Exception as error:
            logging.error(error)
