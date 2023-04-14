import asyncio

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

import django_setup
from tgbot.config import load_config
from tgbot.filters.admin import AdminFilter
from tgbot.filters.lesson import LessonFilter
from tgbot.handlers.admin import register_admin
from tgbot.handlers.catch_lesson import register_catch_lesson_after_inline_mode
from tgbot.handlers.lesson_callbacks import register_handle_lesson
from tgbot.handlers.start_menu_callbacks import register_catch_user_callbacks
from tgbot.handlers.echo import register_echo
from tgbot.handlers.operations_with_photo import register_get_photo_id
from tgbot.handlers.searching_lessons import register_searching
from tgbot.handlers.theme_callbacks import register_handle_themes_or_profile
from tgbot.handlers.user import register_user
from tgbot.integrations.telegraph.abstract import FileUploader
from tgbot.integrations.telegraph.client import TelegraphService
from tgbot.middlewares.environment import EnvironmentMiddleware
from tgbot.middlewares.integrations import IntegrationMiddleware
from tgbot.middlewares.users_manage import UsersManageMiddleware
from tgbot.misc.set_bot_commands import set_default_commands
from tgbot.misc.notify_admins import notify_admins
from tgbot.services.logging import logger


async def on_shutdown(dp: Dispatcher):
    file_uploader: FileUploader = dp.bot["file_uploader"]
    await file_uploader.close()


def register_all_middlewares(dp, config):
    dp.setup_middleware(EnvironmentMiddleware(config=config))
    dp.setup_middleware(UsersManageMiddleware())


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(LessonFilter)


def register_all_handlers(dp):
    # register_admin(dp)
    register_user(dp)
    register_get_photo_id(dp)
    register_catch_user_callbacks(dp)
    register_catch_lesson_after_inline_mode(dp)
    register_handle_themes_or_profile(dp)
    register_handle_lesson(dp)

    register_searching(dp)

    # register_echo(dp)


async def main():
    logger.info("Starting bot")
    config = load_config(".env")

    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    file_uploader = TelegraphService()
    dp = Dispatcher(bot, storage=storage)
    dp.middleware.setup(IntegrationMiddleware(file_uploader))
    bot['config'] = config
    bot['file_uploader'] = file_uploader

    register_all_middlewares(dp, config)
    register_all_filters(dp)
    register_all_handlers(dp)

    await set_default_commands(dp)
    await notify_admins(dp)

    # start
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()
        await on_shutdown(dp)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
