"""
VideoPlayerBot, Telegram Video Chat Bot
Copyright (c) 2021  Asm Safone <https://github.com/AsmSafone>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>
"""

import asyncio
from config import Config
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors import MessageNotModified

CHAT_ID = Config.CHAT_ID
USERNAME = Config.BOT_USERNAME
HOME_TEXT = "👋🏻 **Hi [{}](tg://user?id={})**,\n\nI'm **Video Player Bot**. \nI Can Stream Videos On Telegram Voice Chat. Made With ❤️ By @AsmSafone 😉!"
HELP_TEXT = """
🏷️ --**Setting Up**-- :

\u2022 Start a voice chat in your channel or group.
\u2022 Add bot and user account in chat with admin rights.
\u2022 Then use /stream commands as a reply to an video file.

🏷️ --**Common Commands**-- :

\u2022 `/start` - start the bot
\u2022 `/help` - show this help message
\u2022 `/video` [name] - download the video

🏷️ --**Admin Only Commands**-- :

\u2022 `/stream` - stream the replied video
\u2022 `/mute` - mute the userbot in vc
\u2022 `/unmute` - unmute the userbot in vc
\u2022 `/endstream` - end stream and left vc

© **Powered By** : 
**@AsmSafone | @SafoTheBot** 👑
"""


@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    if query.data=="help":
        buttons = [
            [
                InlineKeyboardButton("CHANNEL", url="https://t.me/AsmSafone"),
                InlineKeyboardButton("SUPPORT", url="https://t.me/SafoTheBot"),
            ],
            [
                InlineKeyboardButton("MORE BOTS", url="https://t.me/AsmSafone/173"),
                InlineKeyboardButton("SOURCE CODE", url="https://github.com/AsmSafone/VideoPlayerBot"),
            ],
            [
                InlineKeyboardButton("BACK HOME", callback_data="home"),
                InlineKeyboardButton("CLOSE MENU", callback_data="close"),
            ]
            ]
        reply_markup = InlineKeyboardMarkup(buttons)
        try:
            await query.edit_message_text(
                HELP_TEXT,
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass

    elif query.data=="home":
        buttons = [
            [
                InlineKeyboardButton("HOW TO USE", callback_data="help"),
            ],
            [
                InlineKeyboardButton("CHANNEL", url="https://t.me/AsmSafone"),
                InlineKeyboardButton("SUPPORT", url="https://t.me/SafoTheBot"),
            ],
            [
                InlineKeyboardButton("MORE BOTS", url="https://t.me/AsmSafone/173"),
                InlineKeyboardButton("SOURCE CODE", url="https://github.com/AsmSafone/VideoPlayerBot"),
            ],
            [
                InlineKeyboardButton("CLOSE MENU", callback_data="close"),
            ]
            ]
        reply_markup = InlineKeyboardMarkup(buttons)
        try:
            await query.edit_message_text(
                HOME_TEXT.format(query.from_user.first_name, query.from_user.id),
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass

    elif query.data=="close":
        try:
            await query.message.delete()
            await query.message.reply_to_message.delete()
        except:
            pass


@Client.on_message(filters.command(["start", f"start@{USERNAME}"]) & (filters.chat(CHAT_ID) | filters.private))
async def start(client, message):
    buttons = [
            [
                InlineKeyboardButton("HOW TO USE", callback_data="help"),
            ],
            [
                InlineKeyboardButton("CHANNEL", url="https://t.me/AsmSafone"),
                InlineKeyboardButton("SUPPORT", url="https://t.me/SafoTheBot"),
            ],
            [
                InlineKeyboardButton("MORE BOTS", url="https://t.me/AsmSafone/173"),
                InlineKeyboardButton("SOURCE CODE", url="https://github.com/AsmSafone/VideoPlayerBot"),
            ],
            [
                InlineKeyboardButton("CLOSE MENU", callback_data="close"),
            ]
            ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await message.reply_text(text=HOME_TEXT.format(message.from_user.first_name, message.from_user.id), reply_markup=reply_markup)

@Client.on_message(filters.command(["help", f"help@{USERNAME}"]) & (filters.chat(CHAT_ID) | filters.private))
async def help(client, message):
    buttons = [
            [
                InlineKeyboardButton("CHANNEL", url="https://t.me/AsmSafone"),
                InlineKeyboardButton("SUPPORT", url="https://t.me/SafoTheBot"),
            ],
            [
                InlineKeyboardButton("MORE BOTS", url="https://t.me/AsmSafone/173"),
                InlineKeyboardButton("SOURCE CODE", url="https://github.com/AsmSafone/VideoPlayerBot"),
            ],
            [
                InlineKeyboardButton("BACK HOME", callback_data="home"),
                InlineKeyboardButton("CLOSE MENU", callback_data="close"),
            ]
            ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await message.reply_text(text=HELP_TEXT, reply_markup=reply_markup)
