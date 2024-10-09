import logging
import asyncio

from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config_data.config import Config, load_config
from keyboards.main_menu import setup_main_menu
from handlers.user import user_rout

logger = logging.getLogger(__name__)

async def main() -> None:
    
    logging.basicConfig(
        level = logging.DEBUG,
        format = '%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s'
    )
    logger.info('Starting Bot')

    config: Config = load_config()

    bot = Bot(token = config.tg_bot.token,
              default = DefaultBotProperties(parse_mode=ParseMode.HTML,
                                             link_preview_is_disabled=True))
    dp = Dispatcher()

    await setup_main_menu(bot)

    dp.include_router(user_rout)

    await dp.start_polling(bot)

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print('Exit')