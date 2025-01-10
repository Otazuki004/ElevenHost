from pyrogram import *
from .. import *

def qfilter(inlineQuery):
    async def funcMano(_, __, query):
        try: return str(query.query).startswith(inlineQuery)
        except: return str(query.data).startswith(inlineQuery)
    return filters.create(funcMano)
