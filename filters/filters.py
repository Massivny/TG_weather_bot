import logging
import re

from aiogram.filters import BaseFilter
from aiogram.types import Message

logger = logging.getLogger(__name__)

class CoordFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        logger.debug('Попали внутрь фильтра %s', __class__.__name__)
        return re.search(r'([-+]?\d{1,2}\.\d+),\s*([-+]?\d{1,3}\.\d+)', message.text)