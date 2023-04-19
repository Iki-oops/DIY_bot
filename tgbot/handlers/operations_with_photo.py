import re

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from tgbot.integrations.telegraph.abstract import FileUploader

from tgbot.models.db_commands import (
    get_or_create_photo,
    get_or_create_photo_pack
)


# Получение photo_id
async def ask_photo_for_file_id(message: types.Message, state: FSMContext):
    await message.answer('Отправьте ваше фото/изображение в формате .jpg/.png')
    await state.set_state('photo_id')


async def get_photo_id(message: types.Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    await message.reply(f'Ваше photo_id: <code>{photo_id}</code>')
    await state.finish()


async def incorrect_photo(message: types.Message):
    await message.reply(
        f'Отправьте фото/изображение. '
        f'Ваш тип контента {message.content_type}\n'
        f'И с правильным форматом тип_изображения|пак_изображения.\n'
        f'Ваш формат: {message.caption}'
    )


# Загрузка фото на сервер
async def ask_photo_for_upload(message: types.Message, state: FSMContext):
    await message.answer('Отправьте фото/изображение '
                         'в формате .jpg/.png 🕵🏻‍♂️\n'
                         'И в caption добавьте '
                         'тип_фотографии|пак_изображения.😇')
    await state.set_state('upload_photo')


async def get_upload_photo_and_url(message: types.Message,
                                   file_uploader: FileUploader,
                                   state: FSMContext):
    photo = message.photo[-1]
    caption = message.caption
    type_photo, name_photo_pack = caption.split('|')

    await message.bot.send_chat_action(message.chat.id, 'upload_photo')

    uploaded_photo = await file_uploader.upload_photo(photo)
    link = uploaded_photo.link
    await message.answer(text=link)
    await state.finish()

    photo_pack = await get_or_create_photo_pack(name=name_photo_pack)
    await get_or_create_photo(link, type_photo, photo_pack[0])


def register_get_photo_id(dp: Dispatcher):
    dp.register_message_handler(ask_photo_for_file_id, Command('get_photo_id'))
    dp.register_message_handler(
        get_photo_id, state='photo_id', content_types=types.ContentTypes.PHOTO
    )

    dp.register_message_handler(ask_photo_for_upload, Command('upload_photo'))
    dp.register_message_handler(
        get_upload_photo_and_url,
        state='upload_photo',
        regexp=re.compile(r'^[a-zA-Zа-яА-Я0-9]{3,}|[a-zA-Zа-яА-Я0-9]{3,}$'),
        content_types=types.ContentTypes.PHOTO
    )

    dp.register_message_handler(
        incorrect_photo,
        state=['photo_id', 'upload_photo'],
        content_types=types.ContentTypes.ANY
    )
