from aiogram import types, Dispatcher


# Закоментировал не пользовательские команды
async def set_default_commands(dp: Dispatcher):
    await dp.bot.set_my_commands(
        [
            types.BotCommand('start', 'Запустить бота'),
            # types.BotCommand('get_photo_id', 'Получить id фото'),
            # types.BotCommand('upload_photo',
            #                  'Скачать на сервер фото и получить url')
        ]
    )
