from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command


# Получение photo_id
from tgbot.integrations.telegraph.abstract import FileUploader


async def ask_photo_for_file_id(message: types.Message, state: FSMContext):
    await message.answer('Отправьте ваше фото/изображение в формате .jpg/.png')
    await state.set_state('photo_id')


async def get_photo_id(message: types.Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    await message.reply(f'Ваше photo_id: <code>{photo_id}</code>')
    await state.finish()


async def incorrect_photo(message: types.Message):
    await message.reply(f'Отправьте фото/изображение, а не {message.content_type}')


# Загрузка фото на сервер
async def ask_photo_for_upload(message: types.Message, state: FSMContext):
    await message.answer('Отправьте фото/изображение в формате .jpg/.png')
    await state.set_state('upload_photo')


async def get_upload_photo_and_url(message: types.Message, file_uploader: FileUploader, state: FSMContext):
    photo = message.photo[-1]
    await message.bot.send_chat_action(message.chat.id, 'upload_photo')
    uploaded_photo = await file_uploader.upload_photo(photo)
    await message.answer(text=uploaded_photo.link)
    await state.finish()


def register_get_photo_id(dp: Dispatcher):
    dp.register_message_handler(ask_photo_for_file_id, Command('get_photo_id'))
    dp.register_message_handler(get_photo_id, state='photo_id', content_types=types.ContentTypes.PHOTO)

    dp.register_message_handler(ask_photo_for_upload, Command('upload_photo'))
    dp.register_message_handler(get_upload_photo_and_url, state='upload_photo', content_types=types.ContentTypes.PHOTO)

    dp.register_message_handler(incorrect_photo, state=['photo_id', 'upload_photo'],
                                content_types=types.ContentTypes.ANY)