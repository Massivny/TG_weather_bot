from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

other_rout = Router()

@other_rout.message()
async def everything_else(msg: Message):
    await msg.answer(text=
                     f'You know, {msg.from_user.first_name}, i\'m a pretty limited bot\n\n'
                     f'if you want to view a list of avaliable commands send me /help')