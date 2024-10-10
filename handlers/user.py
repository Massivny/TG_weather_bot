import requests
import time
import re

from copy import deepcopy
from aiogram import Router, F
from aiogram.filters import Command, StateFilter, or_f, invert_f, and_f
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.dialects.postgresql import insert

from states.states import FSMAddLocation
from lexicon.lexicon import Lexicon_info, Lexicon_cmd_main_menu
from keyboards.keyboard import kb_loc, create_edit_keyboard, create_locations_keyboard
from filters.filters import CoordFilter, DelLocationFilter, LocationFilter
from services.services import get_coords, get_request
from database.models import users_db, users_loc_template, users

user_rout = Router()

################################################################################################################################################
#           MESSAGES 
############################################################################################################################################### 

@user_rout.message(Command('start'))
async def start_cmd(msg: Message, db_engine: AsyncEngine):
    await msg.answer(text = Lexicon_info.Commands['start'])
    if msg.from_user.id not in users_db:
        stmt = insert(users).values(
            telegram_id = msg.from_user.id,
            first_name = msg.from_user.first_name,
            last_name = msg.from_user.last_name
        )

        update_stmt = stmt.on_conflict_do_update(
            index_elements=['telegram_id'],
            set_={
                'first_name': msg.from_user.first_name,
                'last_name': msg.from_user.last_name
            }
        )

        async with db_engine.connect() as conn:
            await conn.execute(update_stmt)
            await conn.commit()

        users_db[msg.from_user.id] = deepcopy(users_loc_template)

@user_rout.message(Command('locations'))
async def loc_cmd(msg: Message):
    await msg.answer(text=Lexicon_info.Commands['locations'],
                     reply_markup=create_locations_keyboard(
                                  *users_db[msg.from_user.id]
                     )
    )   

@user_rout.message(Command('getforecast'))
async def getforecast_cmd(msg: Message):
    pass

@user_rout.message(Command('getfurtherforecast'))
async def getfurtherforecast_cmd(msg: Message):
    pass

@user_rout.message(Command('help'))
async def help_cmd(msg: Message):
    await msg.answer(text = Lexicon_info.Commands['help'])

@user_rout.message(and_f(StateFilter(FSMAddLocation.name),F.text))
async def add_name_proc(msg: Message, state: FSMContext):
    if msg.text not in users_db.get(msg.from_user.id, {}):
        await state.update_data(location_name=msg.text)
        await state.set_state(FSMAddLocation.coordinates)
        await msg.answer(text=Lexicon_info.Commands['addlocation'],
                    reply_markup=kb_loc) 
    else:
        await msg.answer('You already have a location with this name\n'
                         'Try another one')    

@user_rout.message(and_f(StateFilter(FSMAddLocation.coordinates), or_f(F.location, CoordFilter())))
async def add_coord_proc(msg: Message, state: FSMContext):
    coord: dict[str: int] = get_coords(msg=msg)
    data = await state.get_data()
    loc_name = data.get('location_name')
    users_db[msg.from_user.id][loc_name] = coord

    await state.clear()
    await msg.answer(text=f'Location {loc_name} has been added!',
                     reply_markup=ReplyKeyboardRemove())
    
    await msg.answer(text=Lexicon_info.Commands['locations'],
                        reply_markup = create_locations_keyboard(
                                         *users_db[msg.from_user.id])
    )

################################################################################################################################################
#           CALLBACK_QUERY 
##################################a############################################################################################################# 

@user_rout.callback_query(F.data == 'add_location')
async def cb_add_loc(callback: CallbackQuery, state: FSMContext):
    if len(users_db[callback.from_user.id]) < 5:
        await callback.message.delete()
        await state.set_state(FSMAddLocation.name)
        await callback.message.answer('Send location\'s name')
    else:
        await callback.message.answer(text=Lexicon_info.Commands['outofloc'],
                         reply_markup=create_edit_keyboard(
                             *users_db[callback.from_user.id]
                         )
        )
    await callback.answer()

@user_rout.callback_query(F.data == 'edit_locations')
async def cb_edit_loc(callback: CallbackQuery):
    await callback.message.edit_text(
        text = Lexicon_info.Commands[callback.data],
        reply_markup = create_edit_keyboard(
            *users_db[callback.from_user.id]
        )
    )

@user_rout.callback_query(F.data == 'cancel')
async def cb_cancel(callback: CallbackQuery):
    await callback.message.edit_text(Lexicon_info.Commands['help'])
    
@user_rout.callback_query(F.data == 'back')
async def cb_back(callback: CallbackQuery):
    await callback.message.edit_text(text = Lexicon_info.Commands['locations'],
                                     reply_markup=create_locations_keyboard(
                                         *users_db[callback.from_user.id]
                                     )
    ) 
    await callback.answer()

@user_rout.callback_query(DelLocationFilter())
async def cb_remove_loc(callback: CallbackQuery):
    if callback.data[:-3] in users_db[callback.from_user.id]:
        del users_db[callback.from_user.id][callback.data[:-3]]
    await callback.message.edit_text(
          text = Lexicon_info.Commands['edit_locations'],
          reply_markup = create_edit_keyboard(
                *users_db[callback.from_user.id]
          )
    )

@user_rout.callback_query(LocationFilter())
async def cb_loc_proc(callback: CallbackQuery):
    try: 
        await callback.message.edit_text(
            text=get_request(callback.from_user.id, callback.data),
            reply_markup = create_locations_keyboard(
                       *users_db[callback.from_user.id]
            )
        )
    except TelegramBadRequest:
        await callback.answer()
    