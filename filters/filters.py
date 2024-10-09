import logging
import re

from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from database.models import users_db

logger = logging.getLogger(__name__)

class DelLocationFilter(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.endswith('del')
    
class LocationFilter(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
         #logger.debug('Entered filter %s', __class__.__name__)
         if users_db[callback.from_user.id]:
             for loc in users_db[callback.from_user.id]:
                 if str(loc) == callback.data:
                     return True
         return False


class CoordFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        #logger.debug('Попали внутрь фильтра %s', __class__.__name__)
        return re.search(r'([-+]?\d{1,2}\.\d+),\s*([-+]?\d{1,3}\.\d+)', message.text)