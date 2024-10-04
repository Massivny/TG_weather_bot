from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
 
class FSMAddLocation(StatesGroup):
    coordinates = State()
    name = State()
    location = State()
