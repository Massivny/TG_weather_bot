import logging 

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from lexicon.lexicon import Lexicon_cmd_main_menu, Lexicon_info

shareloc_but = KeyboardButton(
    text='Share location',
    request_location=True,
    #one_time_keyboard=True,
)

buttons: list[KeyboardButton] = {
    shareloc_but
}

kb_loc = ReplyKeyboardMarkup(keyboard=[buttons],
                             resize_keyboard=True)