import typing

from aiogram.dispatcher.filters import BoundFilter

from tgbot.config import Config


class LessonFilter(BoundFilter):
    key = 'is_lesson'

    def __init__(self, is_lesson: typing.Optional[bool] = None):
        self.is_lesson = is_lesson

    async def check(self, obj):
        if self.is_lesson is None:
            return False
        try:
            array = obj.text.split('|')
            config: Config = obj.bot.get('config')
            return (obj.via_bot.id == config.tg_bot.bot_id
                    and 'lesson' in array)
        except AttributeError:
            return False

