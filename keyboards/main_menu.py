from aiogram import Bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand

from lexicon.lexicon import Lexicon_cmd_main_menu

async def setup_main_menu(bot: Bot):
    main_menu_cmd = [BotCommand(
        command=command,
        description=description
    ) for command, 
    description in Lexicon_cmd_main_menu.Commands.items()] 
    await bot.set_my_commands(main_menu_cmd)