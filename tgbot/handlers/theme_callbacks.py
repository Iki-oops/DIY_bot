from aiogram import types, Dispatcher
from aiogram.types import InputMediaPhoto
from django.core.paginator import Paginator

from tgbot.keyboards.callback_datas import lesson_callback_data
from tgbot.keyboards.inline_keyboards import category_inline_keyboard
from tgbot.misc.utils import prepare_default_data
from tgbot.models.db_commands import get_themes


async def handle_themes_or_profile(call: types.CallbackQuery,
                                   callback_data: dict):
    await call.answer()

    data = prepare_default_data(callback_data, key='themes_pagination')
    if data.get('category') == 'themes':
        caption = ('Все темы, которые есть в базе 😎\n'
                   'Выбирай интересующую тебя область 😏👇')
        photo = call.bot.get('config').misc.themes_photo
        page = data.get('page')

        objects = await get_themes()
        pagination = Paginator(objects, 15)
        curr_page = pagination.get_page(page)
        await call.message.edit_media(
            media=InputMediaPhoto(
                media=photo,
                caption=caption
            ),
            reply_markup=category_inline_keyboard(data, curr_page),
        )
    else:
        caption = ('Здесь находятся все твои начинания, 🥳\n'
                   'добавленные в избранное и законченные')
        photo = call.bot.get('config').misc.profile_photo

        await call.message.edit_media(
            media=InputMediaPhoto(
                media=photo,
                caption=caption
            ),
            reply_markup=category_inline_keyboard(data),
        )


def register_handle_themes_or_profile(dp: Dispatcher):
    dp.register_callback_query_handler(
        handle_themes_or_profile,
        lesson_callback_data.filter(key='themes_pagination')
    )
