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
import asyncio
from config import Config
from datetime import datetime
from helpers.log import LOGGER
from youtube_dl import YoutubeDL
from pyrogram.types import Message
from pyrogram import Client, filters
from youtube_search import YoutubeSearch
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from helpers.utils import delete, download, get_admins, is_admin, get_buttons, get_link, leave_call, play, get_playlist_str, send_playlist, shuffle_playlist, start_stream, stream_from_link

admin_filter=filters.create(is_admin)


@Client.on_message(filters.command(["play", f"play@{Config.BOT_USERNAME}"]) & (filters.chat(Config.CHAT_ID) | filters.private | filters.chat(Config.LOG_GROUP)))
async def add_to_playlist(_, message: Message):
    if Config.ADMIN_ONLY == "True":
        admins = await get_admins(Config.CHAT_ID)
        if message.from_user.id not in admins:
            k=await message.reply_sticker("CAACAgUAAxkBAAEBpyZhF4R-ZbS5HUrOxI_MSQ10hQt65QACcAMAApOsoVSPUT5eqj5H0h4E")
            await delete(k)
            return
    type=""
    yturl=""
    ysearch=""
    if message.reply_to_message and message.reply_to_message.video:
        msg = await message.reply_text("⚡️")
        type='video'
        m_video = message.reply_to_message.video       
    elif message.reply_to_message and message.reply_to_message.document:
        msg = await message.reply_text("⚡️")
        m_video = message.reply_to_message.document
        type='video'
        if not "video" in m_video.mime_type:
            k=await msg.edit("⛔️ **Invalid Video File Provided !**")
            await delete(k)
            return
    else:
        if message.reply_to_message:
            link=message.reply_to_message.text
            regex = r"^(?:https?:\/\/)?(?:www\.)?youtu\.?be(?:\.com)?\/?.*(?:watch|embed)?(?:.*v=|v\/|\/)([\w\-_]+)\&?"
            match = re.match(regex,link)
            if match:
                type="youtube"
                yturl=link
        elif " " in message.text:
            text = message.text.split(" ", 1)
            query = text[1]
            regex = r"^(?:https?:\/\/)?(?:www\.)?youtu\.?be(?:\.com)?\/?.*(?:watch|embed)?(?:.*v=|v\/|\/)([\w\-_]+)\&?"
            match = re.match(regex,query)
            if match:
                type="youtube"
                yturl=query
            else:
                type="query"
                ysearch=query
        else:
            k=await message.reply_text("❗ __**Send Me An YouTube Video Name / YouTube Video Link / Reply To Video To Play In Telegram Video Chat !**__")
            await delete(k)
            return
    user=f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
    if type=="video":
        now = datetime.now()
        lel = now.strftime("%d-%m-%Y-%H:%M:%S")
        data={1:m_video.file_name, 2:m_video.file_id, 3:"telegram", 4:user, 5:f"{lel}_{m_video.file_size}"}
        Config.playlist.append(data)
        await msg.edit("➕ **Media Added To Playlist !**")
    if type=="youtube" or type=="query":
        if type=="youtube":
            msg = await message.reply_text("🔎")
            url=yturl
        elif type=="query":
            try:
                msg = await message.reply_text("🔎")
                ytquery=ysearch
                results = YoutubeSearch(ytquery, max_results=1).to_dict()
                url = f"https://youtube.com{results[0]['url_suffix']}"
                title = results[0]["title"][:40]
            except Exception as e:
                k=await msg.edit(
                    "**Literary Found Noting !\nTry Searching On Inline Mode 😉!**"
                )
                LOGGER.error(str(e))
                await delete(k)
                return
        else:
            return
        ydl_opts = {
            "geo-bypass": True,
            "nocheckcertificate": True
        }
        ydl = YoutubeDL(ydl_opts)
        try:
            info = ydl.extract_info(url, False)
        except Exception as e:
            LOGGER.error(e)
            k=await msg.edit(
                f"❌ **YouTube Download Error !** \n\n{e}"
                )
            LOGGER.error(str(e))
            await delete(k)
            return
        title = info["title"]
        now = datetime.now()
        lel = now.strftime("%d-%m-%Y-%H:%M:%S")
        data={1:title, 2:url, 3:"youtube", 4:user, 5:f"{lel}_{message.from_user.id}"}
        Config.playlist.append(data)
        await msg.edit(f"➕ **[{title}]({url}) Added To Playlist !**", disable_web_page_preview=True)
    if len(Config.playlist) == 1:
        m_status = await msg.edit("⚡️")
        await download(Config.playlist[0], m_status)
        await m_status.delete()
        await play()
    else:
        await send_playlist()
        await delete(msg)
    pl=await get_playlist_str()
    if message.chat.type == "private":
        await message.reply_photo(photo=Config.THUMB_LINK, caption=pl, reply_markup=await get_buttons())
    elif not Config.LOG_GROUP and message.chat.type == "supergroup":
        await message.reply_photo(photo=Config.THUMB_LINK, caption=pl, reply_markup=await get_buttons())
    await delete(message)
    for track in Config.playlist[:2]:
        await download(track)


@Client.on_message(filters.command(["leave", f"leave@{Config.BOT_USERNAME}"]) & admin_filter & (filters.chat(Config.CHAT_ID) | filters.private | filters.chat(Config.LOG_GROUP)))
async def leave_voice_chat(_, m: Message):
    if not Config.CALL_STATUS:
        k=await m.reply_text("🤖 **Didn't Joined Video Chat !**")
        await delete(k)
        return
    await leave_call()
    k=await m.reply_text("✅ **Left From Video Chat !**")
    await delete(k)


@Client.on_message(filters.command(["shuffle", f"shuffle@{Config.BOT_USERNAME}"]) & admin_filter & (filters.chat(Config.CHAT_ID) | filters.private | filters.chat(Config.LOG_GROUP)))
async def shuffle_play_list(client, m: Message):
    if not Config.CALL_STATUS:
        k=await m.reply_text("🤖 **Didn't Joined Video Chat !**")
        await delete(k)
    else:
        if len(Config.playlist) > 2:
            await shuffle_playlist()
            k=await m.reply_text(f"🔄 **Playlist Shuffled !**")
            await delete(k)
        else:
            k=await m.reply_text(f"⛔️ **Can't Shuffle Playlist For Less Than 3 Video !**")
            await delete(k)


@Client.on_message(filters.command(["clrlist", f"clrlist@{Config.BOT_USERNAME}"]) & admin_filter & (filters.chat(Config.CHAT_ID) | filters.private | filters.chat(Config.LOG_GROUP)))
async def clear_play_list(client, m: Message):
    if not Config.CALL_STATUS:
        k=await m.reply_text("🤖 **Didn't Joined Video Chat !**")
        await delete(k)
        return
    if not Config.playlist:
        k=await m.reply_text("⛔️ **Empty Playlist !**")
        await delete(k)
        return
    Config.playlist.clear()   
    k=await m.reply_text(f"✅ **Playlist Cleared !**")
    await delete(k)
    await start_stream()


@Client.on_message(filters.command(["stream", f"stream@{Config.BOT_USERNAME}"]) & admin_filter & (filters.chat(Config.CHAT_ID) | filters.private | filters.chat(Config.LOG_GROUP)))
async def stream(client, m: Message):
    if m.reply_to_message:
        link=m.reply_to_message.text
    elif " " in m.text:
        text = m.text.split(" ", 1)
        link = text[1]
    else:
        k=await m.reply_text("❗ __**Send Me An Live Stream Link / YouTube Live Stream Link To Start Live Streaming !**__")
        await delete(k)
        return
    regex = r"^(?:https?:\/\/)?(?:www\.)?youtu\.?be(?:\.com)?\/?.*(?:watch|embed)?(?:.*v=|v\/|\/)([\w\-_]+)\&?"
    match = re.match(regex,link)
    if match:
        stream_link=await get_link(link)
        if not stream_link:
            k=await m.reply_text("⛔️ **Invalid Stream Link Provided !**")
            await delete(k)
            return
    else:
        stream_link=link
    k, msg=await stream_from_link(stream_link)
    if k == False:
        s=await m.reply_text(msg)
        await delete(s)
        return
    s=await m.reply_text(f"▶️ **Started [Live Streaming]({stream_link}) !**", disable_web_page_preview=True)
    await delete(s)


admincmds=["join", "leave", "pause", "resume", "skip", "restart", "volume", "shuffle", "clrlist", "update", "replay", "getlogs", "stream", "mute", "unmute", "seek", f"mute@{Config.BOT_USERNAME}", f"unmute@{Config.BOT_USERNAME}", f"seek@{Config.BOT_USERNAME}", f"stream@{Config.BOT_USERNAME}", f"getlogs@{Config.BOT_USERNAME}", f"replay@{Config.BOT_USERNAME}", f"join@{Config.BOT_USERNAME}", f"leave@{Config.BOT_USERNAME}", f"pause@{Config.BOT_USERNAME}", f"resume@{Config.BOT_USERNAME}", f"skip@{Config.BOT_USERNAME}", f"restart@{Config.BOT_USERNAME}", f"volume@{Config.BOT_USERNAME}", f"shuffle@{Config.BOT_USERNAME}", f"clrlist@{Config.BOT_USERNAME}", f"update@{Config.BOT_USERNAME}"]

@Client.on_message(filters.command(admincmds) & ~admin_filter & (filters.chat(Config.CHAT_ID) | filters.private | filters.chat(Config.LOG_GROUP)))
async def notforu(_, m: Message):
    k=await _.send_cached_media(chat_id=m.chat.id, file_id="CAACAgUAAxkBAAEB1GNhO2oHEh2OqrpucczIprmOIEKZtQACfwMAAjSe9DFG-UktB_TxOh4E", caption="**You Are Not Authorized !!**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('⚡️ Join Here ⚡️', url='https://t.me/AsmSafone')]]), reply_to_message_id=m.message_id)
    await delete(k)

allcmd = ["play", "current", "playlist", f"play@{Config.BOT_USERNAME}", f"current@{Config.BOT_USERNAME}", f"playlist@{Config.BOT_USERNAME}"] + admincmds

@Client.on_message(filters.command(allcmd) & filters.group & ~(filters.chat(Config.CHAT_ID) | filters.private | filters.chat(Config.LOG_GROUP)))
async def not_chat(_, m: Message):
    buttons = [
            [
                InlineKeyboardButton("CHANNEL", url="https://t.me/AsmSafone"),
                InlineKeyboardButton("SUPPORT", url="https://t.me/SafoTheBot"),
            ],
            [
                InlineKeyboardButton("🤖 MAKE YOUR OWN BOT 🤖", url="https://heroku.com/deploy?template=https://github.com/AsmSafone/VideoPlayerBot/tree/alpha"),
            ]
         ]
    await m.reply_text(text="**Sorry, You Can't Use This Bot In This Group 🤷‍♂️! But You Can Make Your Own Bot Like This From The [Source Code](https://github.com/AsmSafone/VideoPlayerBot/tree/alpha) Below 😉!**", reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)
