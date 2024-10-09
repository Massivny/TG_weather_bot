import logging 

from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup,
                           InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon import Lexicon_but, Lexicon_info

shareloc_but = KeyboardButton(
    text='Share location',
    request_location=True,
)

buttons: list[KeyboardButton] = {
    shareloc_but
}

kb_loc = ReplyKeyboardMarkup(keyboard=[buttons],
                             resize_keyboard=True)

def create_locations_keyboard(*args: int) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    if args:
        for loc in args:
            kb_builder.row(InlineKeyboardButton(
                text = f'{loc}',
                callback_data = str(loc)
            ))
    kb_builder.row(
        InlineKeyboardButton(
            text = Lexicon_but.Commands['addlocation_but'],
            callback_data = 'add_location'
        ),
        InlineKeyboardButton(
            text = Lexicon_but.Commands['edit_locations_but'],
            callback_data = 'edit_locations'
        ),
        InlineKeyboardButton(
            text = Lexicon_but.Commands['cancel_but'],
            callback_data = 'cancel'
        ),
        width=3,
    )
    return kb_builder.as_markup()

def create_edit_keyboard(*args: int) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    if args:
        for loc in args:
            kb_builder.row(InlineKeyboardButton(
                text = f'{Lexicon_but.Commands['del_but']} {loc}',
                callback_data = f'{loc}del'
            ))
    kb_builder.row(
        InlineKeyboardButton(
            text = Lexicon_but.Commands['cancel_but'],
            callback_data = 'cancel'
        ),
        InlineKeyboardButton(
            text = Lexicon_but.Commands['back_but'],
            callback_data = 'back' 
        ),
        width=2
    )
    return kb_builder.as_markup()
