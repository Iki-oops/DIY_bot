from typing import Union

from aiogram import Dispatcher, types
from aiogram.types import InputMediaPhoto

from tgbot.keyboards.inline_keyboards import start_inline_keyboard


async def user_start(update: Union[types.Message, types.CallbackQuery],
                     *args, **kwargs):
    message = None
    if isinstance(update, types.Message):
        message = update
    elif isinstance(update, types.CallbackQuery):
        message = update.message

    user = message.from_user
    username = user.username
    if user.full_name:
        username = user.full_name

    photo = message.bot.get('config').misc.face_photo
    caption = (f"Привет, <b>{username}</b>👋!\n\n"
               "Это бот архив💾 туториалов и DIY-идей.🪄\n"
               "Здесь ты точно найдешь, чем себя занять!☺️\n\n"
               "<b>!!! Инструкции: !!!</b>")

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
