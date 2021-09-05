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

import os
import re
import time
import ffmpeg
import asyncio
from os import path
from asyncio import sleep
from config import Config
from bot.safone.nopm import User
from youtube_dl import YoutubeDL
from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls import GroupCallFactory
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

ADMINS = Config.ADMINS
CHAT_ID = Config.CHAT_ID
USERNAME = Config.BOT_USERNAME

STREAM = {6}
VIDEO_CALL = {}

ydl_opts = {
        "geo_bypass": True,
        "nocheckcertificate": True,
}
ydl = YoutubeDL(ydl_opts)
group_call_factory = GroupCallFactory(User, GroupCallFactory.MTPROTO_CLIENT_TYPE.PYROGRAM)

@Client.on_message(filters.command(["stream", f"stream@{USERNAME}"]) & filters.user(ADMINS) & (filters.chat(CHAT_ID) | filters.private))
async def stream(client, m: Message):
    if 1 in STREAM:
        await m.reply_text("🤖 **Please Stop The Existing Stream!**")
        return

    media = m.reply_to_message
    if not media and not ' ' in m.text:
        await m.reply_text("❗ __Send Me An YouTube Video Link / Live Stream Link / Reply To An Video To Start Streaming!__")

    elif ' ' in m.text:
        msg = await m.reply_text("🔄 `Processing ...`")
        text = m.text.split(' ', 1)
        query = text[1]
        regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"
        match = re.match(regex,query)
        if match:
            await msg.edit("🔄 `Starting YouTube Stream ...`")
            try:
                meta = ydl.extract_info(query, download=False)
                formats = meta.get('formats', [meta])
                for f in formats:
                        ytstreamlink = f['url']
                ytstream = ytstreamlink
            except Exception as e:
                await msg.edit(f"❌ **YouTube Download Error!** \n\n`{e}`")
                print(e)
                return
            await sleep(2)
            try:
                group_call = group_call_factory.get_group_call()
                await group_call.join(CHAT_ID)
                await group_call.start_video(ytstream)
                VIDEO_CALL[CHAT_ID] = group_call
                await msg.edit(f"▶️ **Started [YouTube Streaming]({query})!**", disable_web_page_preview=True)
                try:
                    STREAM.remove(0)
                except:
                    pass
                try:
                    STREAM.add(1)
                except:
                    pass
            except Exception as e:
                await msg.edit(f"❌ **An Error Occoured!** \n\nError: `{e}`")
        else:
            await msg.edit("🔄 `Starting Live Stream ...`")
            livestream = query
            await sleep(2)
            try:
                group_call = group_call_factory.get_group_call()
                await group_call.join(CHAT_ID)
                await group_call.start_video(livestream)
                VIDEO_CALL[CHAT_ID] = group_call
                await msg.edit(f"▶️ **Started [Live Streaming]({query})!**", disable_web_page_preview=True)
                try:
                    STREAM.remove(0)
                except:
                    pass
                try:
                    STREAM.add(1)
                except:
                    pass
            except Exception as e:
                await msg.edit(f"❌ **An Error Occoured!** \n\nError: `{e}`")

    elif media.video or media.document:
        msg = await m.reply_text("🔄 `Downloading ...`")
        video = await client.download_media(media)
        await sleep(2)
        try:
            group_call = group_call_factory.get_group_call()
            await group_call.join(CHAT_ID)
            await group_call.start_video(video)
            VIDEO_CALL[CHAT_ID] = group_call
            await msg.edit("▶️ **Started Video Streaming!**")
            try:
                STREAM.remove(0)
            except:
                pass
            try:
                STREAM.add(1)
            except:
                pass
        except Exception as e:
            await msg.edit(f"❌ **An Error Occoured!** \n\nError: `{e}`")
    else:
        await m.reply_text("❗ __Send Me An Live Stream Link / YouTube Video Link / Reply To An Video To Start Streaming!__")
        return


@Client.on_message(filters.command(["endstream", f"endstream@{USERNAME}"]) & filters.user(ADMINS) & (filters.chat(CHAT_ID) | filters.private))
async def endstream(client, m: Message):
    if 0 in STREAM:
        await m.reply_text("🤖 **Please Start An Stream First!**")
        return

    msg = await m.reply_text("🔄 `Processing ...`")
    if CHAT_ID in VIDEO_CALL:
        await VIDEO_CALL[CHAT_ID].stop()
        VIDEO_CALL.pop(CHAT_ID)
        await msg.edit("⏹️ **Stopped Video Streaming!**")
        try:
            STREAM.remove(1)
        except:
            pass
        try:
            STREAM.add(0)
        except:
            pass
    else:
        await msg.edit("🤖 **Please Start An Stream First!**")


admincmds=["stream", "radio", "stopradio", "endstream", f"stream@{USERNAME}", f"radio@{USERNAME}", f"stopradio@{USERNAME}", f"endstream@{USERNAME}"]

@Client.on_message(filters.command(admincmds) & ~filters.user(ADMINS) & (filters.chat(CHAT_ID) | filters.private))
async def notforu(_, m: Message):
    k = await m.reply_sticker("CAACAgUAAxkBAAEBpyZhF4R-ZbS5HUrOxI_MSQ10hQt65QACcAMAApOsoVSPUT5eqj5H0h4E")
    await sleep(5)
    await k.delete()
    try:
        await m.delete()
    except:
        pass

allcmd = ["start", "help", f"start@{USERNAME}", f"help@{USERNAME}"] + admincmds

@Client.on_message(filters.command(allcmd) & filters.group & ~filters.chat(CHAT_ID))
async def not_chat(_, m: Message):
    buttons = [
            [
                InlineKeyboardButton("CHANNEL", url="https://t.me/AsmSafone"),
                InlineKeyboardButton("SUPPORT", url="https://t.me/SafoTheBot"),
            ],
            [
                InlineKeyboardButton("🤖 MAKE YOUR OWN BOT 🤖", url="https://heroku.com/deploy?template=https://github.com/AsmSafone/VideoPlayerBot"),
            ]
         ]
    await m.reply_text(text="**Sorry, You Can't Use This Bot In This Group 🤷‍♂️! But You Can Make Your Own Bot Like This From The [Source Code](https://github.com/AsmSafone/VideoPlayerBot) Below 😉!**", reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)
