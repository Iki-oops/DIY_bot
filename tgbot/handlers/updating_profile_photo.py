from aiogram import types
from aiogram.types import InputMediaPhoto
from aiogram.utils.exceptions import MessageNotModified
from django.core.paginator import Paginator

from tgbot.keyboards.dynamic_inline_keyboards import (
    make_dynamic_profiles_inline,
)
from tgbot.models.db_commands import (
    get_user_pack,
    get_photo_packs,
    get_photo_pack, get_photo_via_type_photo,
)


async def update_profile_photo(call: types.CallbackQuery, data: dict):
    await call.answer()
    page, curr_level = data.get('page'), int(data.get('level'))

    user_pack = await get_user_pack(call.from_user.id)
    photo_pack = user_pack.photo_pack

    new_pack_id = int(data.get('item_id'))

    profile_photos = await get_photo_packs()

    if new_pack_id != photo_pack.id and new_pack_id:
        for profile_photo in profile_photos:
            if profile_photo.id == new_pack_id:
                user_pack.photo_pack = await get_photo_pack(new_pack_id)
                user_pack.save()
                photo_pack = user_pack.photo_pack

    for profile_photo in profile_photos:
        if profile_photo.id == photo_pack.id:
            profile_photo.name = '✅ ' + profile_photo.name

    paginator = Paginator(profile_photos, 15)
    curr_page = paginator.get_page(page)

    try:
        try:
            photo = await get_photo_via_type_photo(
                call.from_user.id, 'set_profile_photo')
        except Exception:
            photo = call.bot.get('config').misc.set_profile_photo

        caption = ('Здесь ты можешь поменять пак изображений 😼\n'
                   'Выбирай подходящий тебе пак изображений 🥳')

        await call.message.edit_media(
            media=InputMediaPhoto(
                media=photo,
                caption=caption,
            ),
            reply_markup=make_dynamic_profiles_inline(
                curr_page, curr_level, data
            )
        )
    except MessageNotModified:
        pass
