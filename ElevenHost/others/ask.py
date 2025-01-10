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

async def ask(message=None, text=None, chat=None, user=None):
    global datas
    chat_id = chat or message.chat.id
    user_id = user or message.from_user.id
    
    if text: await otazuki.send_message(chat_id, text)
    
    datas[user_id] = {}
    datas[user_id]['chat'] = chat_id
    datas[user_id]['Listen'] = True
    datas[user_id]['message'] = None
    
    logging.info(f"Starting listening for input: {datas}")
    
    while not datas.get(user_id).get('message'):
        await asyncio.sleep(0.3)
    
    res = datas.get(user_id).get('message')
    logging.info(f"Got message {res}")
    del datas[user_id]
    return res

@otazuki.on_message(filters.text & filters.create(ask_helper))
async def ask_helperr(_, m):
    pass
