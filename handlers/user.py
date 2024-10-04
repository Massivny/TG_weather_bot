import requests
import time
import re

from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery, ContentType, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.types.location import Location

from states.states import FSMAddLocation
from lexicon.lexicon import Lexicon_info, Lexicon_cmd_main_menu, get_cmd
from keyboards.keyboard import kb_loc
from filters.filters import CoordFilter

user_rout = Router()

################################################################################################################################################
#           COMMANDS 
############################################################################################################################################### 

@user_rout.message(Command('start'))
async def start_cmd(msg: Message):
    updates: dict = requests.get(f'https://api.tomorrow.io/v4/weather/forecast?location=42.3478,-71.0466&apikey=XVP8767CKD5FSpgcfKxveBYNDYjswBEJ').json()
    if updates:
        for items in updates['timelines']['daily']:
            await msg.answer(str(items['values']['temperatureAvg']))

@user_rout.message(Command('addlocation'))
async def setlocation_cmd(msg: Message, state: FSMContext):
    await msg.answer(text=Lexicon_info.Commands['addlocation'],
                     reply_markup=kb_loc)
    await state.set_state(FSMAddLocation.location)

@user_rout.message(Command('getforecast'))
async def getforecast_cmd(msg: Message):
    pass

@user_rout.message(Command('getfurtherforecast'))
async def getfurtherforecast_cmd(msg: Message):
    pass

@user_rout.message(Command('help'))
async def help_cmd(msg: Message):
    await msg.answer(text = Lexicon_info.Commands['help'])

@user_rout.message(StateFilter(FSMAddLocation.location) and F.location)
async def add_share_loc_cmd(msg: Message, state: FSMContext):
    if F.location:
        longitude = msg.location.longitude
        latitude = msg.location.latitude
    await msg.answer(text=f'latitude - {latitude}\nlongitude - {longitude}',
                     reply_markup=ReplyKeyboardRemove())
    await state.clear()

@user_rout.message(StateFilter(FSMAddLocation.location) and CoordFilter())
async def add_loc_cmd(msg: Message, state: FSMContext):
    match = re.search(r'([-+]?\d{1,2}\.\d+),\s*([-+]?\d{1,3}\.\d+)', msg.text)
    longitude = match.group(2)
    latitude = match.group(1)
    await msg.answer(text=f'latitude - {latitude}\nlongitude - {longitude}',
                     reply_markup=ReplyKeyboardRemove())
    await state.clear()