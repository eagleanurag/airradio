
from pyrogram import Client, filters, emoji
from pyrogram.types import Message
from utils import mp, RADIO, USERNAME
from config import Config, STREAM

CHAT=Config.CHAT
ADMINS=Config.ADMINS
LOG_GROUP=Config.LOG_GROUP


@Client.on_message(filters.command(["radio", f"radio@{USERNAME}"]) & filters.user(ADMINS) & (filters.chat(CHAT) | filters.private | filters.chat(LOG_GROUP)))
async def radio(client, message: Message):
    if 1 in RADIO:
        k=await message.reply_text(f"{emoji.ROBOT} **Please Stop Existing Radio Stream!**")
        await mp.delete(k)
        await message.delete()
        return
    await mp.start_radio()
    k=await message.reply_text(f"{emoji.CHECK_MARK_BUTTON} **Radio Stream Started :** \n<code>{STREAM}</code>")
    await mp.delete(k)
    await mp.delete(message)

@Client.on_message(filters.command(["stopradio", f"stopradio@{USERNAME}"]) & filters.user(ADMINS) & (filters.chat(CHAT) | filters.private | filters.chat(LOG_GROUP)))
async def stop(_, message: Message):
    if 0 in RADIO:
        k=await message.reply_text(f"{emoji.ROBOT} **Please Start A Radio Stream First!**")
        await mp.delete(k)
        await mp.delete(message)
        return
    await mp.stop_radio()
    k=await message.reply_text(f"{emoji.CROSS_MARK_BUTTON} **Radio Stream Ended Successfully!**")
    await mp.delete(k)
    await mp.delete(message)
