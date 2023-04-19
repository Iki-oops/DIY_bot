from typing import Union

from aiogram import Dispatcher, types
from aiogram.types import InputMediaPhoto

from tgbot.keyboards.inline_keyboards import start_inline_keyboard
from tgbot.models.db_commands import get_photo_via_type_photo


async def user_start(update: Union[types.Message, types.CallbackQuery],
                     *args, **kwargs):
    message = None
    user_id = update.from_user.id
    if isinstance(update, types.Message):
        message = update
    elif isinstance(update, types.CallbackQuery):
        message = update.message

    user = message.from_user
    username = user.username
    if user.full_name:
        username = user.full_name

    try:
        photo = await get_photo_via_type_photo(
            user_id, 'face_photo')
    except Exception:
        photo = message.bot.get('config').misc.face_photo

    caption = (f"Привет, <b>{username}</b>👋!\n\n"
               "Это бот архив💾 туториалов и DIY-идей.🪄\n"
               "Здесь ты точно найдешь, чем себя занять!☺️\n\n"
               "👈 Налево пойдешь \n"
               "   список тем найдешь 🤭\n"
               "   👉 Направо, твои\n"
               "      сохраненные уроки 🕵🏻‍♂️\n"
               "      и настройка изображений\n"
               "      твоего профиля 👨🏼‍🔧\n\n"
               "По середине  👇  тренды и поисковик👮🏻‍♂️\n")

    if isinstance(update, types.CallbackQuery):
        await message.edit_media(
            media=InputMediaPhoto(
                media=photo,
                caption=caption
            ),
            reply_markup=start_inline_keyboard()
        )
        return

    await message.answer_photo(
        photo=photo,
        caption=caption,
        reply_markup=start_inline_keyboard()
    )


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
