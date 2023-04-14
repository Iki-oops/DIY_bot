from aiogram import types
from aiogram.types import InputMediaPhoto

from tgbot.keyboards.inline_keyboards import category_inline_keyboard


async def handle_themes_or_profile(call: types.CallbackQuery,
                                   callback_data: dict):
    await call.answer()

    category = callback_data.get('category')
    if category == 'themes':
        caption = ('Все темы, которые есть в базе 😎\n'
                   'Выбирай интересующую тебя область 😏👇')
        photo = call.bot.get('config').misc.themes_photo
    else:
        caption = ('Здесь находятся все твои начинания, 🥳\n'
                   'добавленные в избранное и законченные')
        photo = call.bot.get('config').misc.profile_photo

    await call.message.edit_media(
        media=InputMediaPhoto(
            media=photo,
            caption=caption
        ),
        reply_markup=await category_inline_keyboard(category),
    )
