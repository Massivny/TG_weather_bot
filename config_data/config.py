from dataclasses import dataclass
from environs import Env

@dataclass
class TgBot():
    token: str

@dataclass
class Database():
    dsn: str

@dataclass
class Config():
    tg_bot: TgBot
    db: Database 

def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        tg_bot=TgBot(token=env('BOT_TOKEN')),
        db=Database(dsn=env('PG_LINK'))
    )