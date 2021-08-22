
import asyncio
from pyrogram import Client, filters, emoji
from utils import USERNAME, mp
from config import Config
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

msg=Config.msg
CHAT=Config.CHAT
ADMINS=Config.ADMINS
playlist=Config.playlist

HOME_TEXT = "👋🏻 **Hi [{}](tg://user?id={})**,\n\nI'm **AIR News V1.0** \nI Can Play News / YouTube Live In Voice Chat 24x7 Nonstop. Made with ❤️ By eagleanurag 😉!"
HELP_TEXT = """
🎧 --**Need Help ?**--
(Join @crack_ssb For Support)

🏷️ --**Common Commands**-- :

\u2022 `/play` - reply to an audio or youTube link to play it or use /play [song name]
\u2022 `/help` - shows help for commands
\u2022 `/song` [song name] - download the song as audio track
\u2022 `/current` - shows playing time of current track
\u2022 `/playlist` - shows the current playlist with controls

🏷️ --**Admin Commands**-- :

\u2022 `/radio` - start radio stream
\u2022 `/stopradio` - stop radio stream
\u2022 `/skip` - skip current music
\u2022 `/join` - join the voice chat
\u2022 `/leave` - leave the voice chat
\u2022 `/stop` - stop playing music
\u2022 `/volume` - change volume (0-200)
\u2022 `/replay` - play from the beginning
\u2022 `/clean` - remove unused raw files
\u2022 `/pause` - pause playing music
\u2022 `/resume` - resume playing music
\u2022 `/mute` - mute the vc userbot
\u2022 `/unmute` - unmute the vc userbot
\u2022 `/restart` - update & restart the bot

© **Powered By** : 
**@crack_ssb | @virtaulGTO2_bot** 👑
"""


@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    if query.from_user.id not in Config.ADMINS and query.data != "help":
        await query.answer(
            "You're Not Allowed! 🤣",
            show_alert=True
            )
        return
    else:
        await query.answer()
    if query.data == "replay":
        group_call = mp.group_call
        if not playlist:
            return
        group_call.restart_playout()
        if not playlist:
            pl = f"{emoji.NO_ENTRY} **Empty Playlist!**"
        else:
            pl = f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
                f"**{i}**. **{x[1]}**\n  - **Requested By:** {x[4]}"
                for i, x in enumerate(playlist)
                ])
        await query.edit_message_text(
                f"{pl}",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🔄", callback_data="replay"),
                            InlineKeyboardButton("⏸", callback_data="pause"),
                            InlineKeyboardButton("⏭", callback_data="skip")
                            
                        ],
                    ]
                )
            )

    elif query.data == "pause":
        if not playlist:
            return
        else:
            mp.group_call.pause_playout()
            pl = f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
                f"**{i}**. **{x[1]}**\n  **Requested By:** {x[4]}"
                for i, x in enumerate(playlist)
                ])
        await query.edit_message_text(f"{emoji.PLAY_OR_PAUSE_BUTTON} **Paused !**\n\n{pl}",
        reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🔄", callback_data="replay"),
                            InlineKeyboardButton("▶️", callback_data="resume"),
                            InlineKeyboardButton("⏭", callback_data="skip")
                            
                        ],
                    ]
                )
            )

    elif query.data == "resume":   
        if not playlist:
            return
        else:
            mp.group_call.resume_playout()
            pl = f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
                f"**{i}**. **{x[1]}**\n  - **Requested By:** {x[4]}"
                for i, x in enumerate(playlist)
                ])
        await query.edit_message_text(f"{emoji.PLAY_OR_PAUSE_BUTTON} **Resumed !**\n\n{pl}",
        reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🔄", callback_data="replay"),
                            InlineKeyboardButton("⏸", callback_data="pause"),
                            InlineKeyboardButton("⏭", callback_data="skip")
                            
                        ],
                    ]
                )
            )

    elif query.data=="skip":   
        if not playlist:
            return
        else:
            await mp.skip_current_playing()
            pl = f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
                f"**{i}**. **{x[1]}**\n  - **Requested By:** {x[4]}"
                for i, x in enumerate(playlist)
                ])
        try:
            await query.edit_message_text(f"{emoji.PLAY_OR_PAUSE_BUTTON} **Skipped !**\n\n{pl}",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🔄", callback_data="replay"),
                        InlineKeyboardButton("⏸", callback_data="pause"),
                        InlineKeyboardButton("⏭", callback_data="skip")
                            
                    ],
                ]
            )
        )
        except:
            pass
    elif query.data=="help":
        buttons = [
            [
                InlineKeyboardButton("CHANNEL", url="https://t.me/crack_ssb"),
                InlineKeyboardButton("SUPPORT", url="https://t.me/virtualGTO2_bot"),
            ],
            [
                InlineKeyboardButton("MORE BOTS", url="https://www.google.com/search?q=eagleanurag"),
                InlineKeyboardButton("SOURCE CODE", url="https://www.google.com/search?q=eagleanurag"),
            ],
            [
                InlineKeyboardButton("CLOSE 🔐", callback_data="close"),
            ]
            ]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.edit_message_text(
            HELP_TEXT,
            reply_markup=reply_markup

        )

    elif query.data=="close":
        await query.message.delete()


@Client.on_message(filters.command(["start", f"start@{USERNAME}"]))
async def start(client, message):
    buttons = [
            [
                InlineKeyboardButton("CHANNEL", url="https://t.me/crack_ssb"),
                InlineKeyboardButton("SUPPORT", url="https://t.me/virtualGTO2_bot"),
            ],
            [
                InlineKeyboardButton("MORE BOTS", url="https://www.google.com/search?q=eagleanurag"),
                InlineKeyboardButton("SOURCE CODE", url="https://www.google.com/search?q=eagleanurag"),
            ],
            [
                InlineKeyboardButton("❔ HOW TO USE ❔", callback_data="help"),
            ]
            ]
    reply_markup = InlineKeyboardMarkup(buttons)
    m=await message.reply_photo(photo="https://telegra.ph/file/7c8f49c2c6a6b8883cb84.jpg", caption=HOME_TEXT.format(message.from_user.first_name, message.from_user.id), reply_markup=reply_markup)
    await mp.delete(m)
    await mp.delete(message)



@Client.on_message(filters.command(["help", f"help@{USERNAME}"]))
async def help(client, message):
    buttons = [
            [
                InlineKeyboardButton("CHANNEL", url="https://t.me/crack_ssb"),
                InlineKeyboardButton("SUPPORT", url="https://t.me/virtualGTO2_bot"),
            ],
            [
                InlineKeyboardButton("MORE BOTS", url="https://www.google.com/search?q=eagleanurag"),
                InlineKeyboardButton("SOURCE CODE", url="https://www.google.com/search?q=eagleanurag"),
            ],
            [
                InlineKeyboardButton("CLOSE 🔐", callback_data="close"),
            ]
            ]
    reply_markup = InlineKeyboardMarkup(buttons)
    if msg.get('help') is not None:
        await msg['help'].delete()
    msg['help'] = await message.reply_photo(photo="https://telegra.ph/file/7c8f49c2c6a6b8883cb84.jpg", caption=HELP_TEXT, reply_markup=reply_markup)
    await mp.delete(message)

