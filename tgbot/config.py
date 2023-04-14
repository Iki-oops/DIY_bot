from dataclasses import dataclass

from environs import Env


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]
    use_redis: bool
    bot_id: int


@dataclass
class Miscellaneous:
    face_photo: str = 'https://telegra.ph//file/f8351e71d66180523bfd2.jpg'
    themes_photo: str = 'https://telegra.ph//file/d94839ef8fd32164e78ce.jpg'
    profile_photo: str = 'https://telegra.ph//file/553a18cb2ce2d147cd51c.jpg'


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    misc: Miscellaneous


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            use_redis=env.bool("USE_REDIS"),
            bot_id=env.int("BOT_ID")
        ),
        db=DbConfig(
            host=env.str('DB_HOST'),
            password=env.str('DB_PASS'),
            user=env.str('DB_USER'),
            database=env.str('DB_NAME')
        ),
        misc=Miscellaneous()
    )
