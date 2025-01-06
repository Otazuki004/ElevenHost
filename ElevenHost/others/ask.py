from pyrogram import *
from ElevenHost import *
import asyncio
import logging

otazuki = app

datas = {}

async def ask_helper(_, client, message):
    global datas
    try:
        if message.text.startswith(('.','!','/')): return False
        if datas.get(message.from_user.id) and datas.get(message.from_user.id).get('chat') == message.chat.id and datas.get(message.from_user.id).get('Listen'):
            datas[message.from_user.id]['message'] = message.text
            datas[message.from_user.id]['Listen'] = False
            return False
        return False
    except: pass

async def ask(message, text=None):
    global datas
    if text: await otazuki.send_message(message.chat.id, text)
    datas[message.from_user.id] = {}
    datas[message.from_user.id]['chat'] = message.chat.id
    datas[message.from_user.id]['Listen'] = True
    datas[message.from_user.id]['message'] = None
    logging.info(f"Starting listening for input: {datas}")
    while not datas.get(message.from_user.id).get('message'):
        await asyncio.sleep(0.3)
    res = datas.get(message.from_user.id).get('message')
    logging.info(f"Got message {res}")
    del datas[message.from_user.id]
    return res

@otazuki.on_message(filters.text & filters.create(ask_helper))
async def ask_helperr(_, m):
    pass
