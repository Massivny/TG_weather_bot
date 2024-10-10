import logging
import asyncio

from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.future import select

from config_data.config import Config, load_config
from keyboards.main_menu import setup_main_menu
from handlers.user import user_rout
from database.models import metadata

logger = logging.getLogger(__name__)

async def main() -> None:
    
    logging.basicConfig(
        level = logging.DEBUG,
        format = '%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s'
    )
    logger.info('Starting Bot')

    config: Config = load_config()

    engine = create_async_engine(
        url=str(config.db.dsn),
        echo=True,
    )

    bot = Bot(token = config.tg_bot.token,
              default = DefaultBotProperties(parse_mode=ParseMode.HTML,
                                             link_preview_is_disabled=True))
    dp = Dispatcher(db_engine=engine)

    await setup_main_menu(bot)

    dp.include_router(user_rout)

    async with engine.begin() as conn:
        result = await conn.execute(select(1))
        print(result.scalar())
    
    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)
        await conn.run_sync(metadata.create_all)

    await dp.start_polling(bot)

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print('Exit')

