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
from helpers.log import LOGGER
from pyrogram.types import Message
from pyrogram import Client, filters
from helpers.utils import delete, get_playlist_str, is_admin, mute, restart_playout, skip, pause, resume, unmute, volume, get_buttons, is_admin, seek_file, get_player_string

admin_filter=filters.create(is_admin)


@Client.on_message(filters.command(["playlist", f"playlist@{Config.BOT_USERNAME}"]) & (filters.chat(Config.CHAT_ID) | filters.private | filters.chat(Config.LOG_GROUP)))
async def c_playlist(client, message):
    pl = await get_playlist_str()
    if message.chat.type == "private":
        await message.reply_text(
            pl,
            disable_web_page_preview=True,
        )
    else:
        if Config.msg.get('playlist') is not None:
            try:
                await Config.msg['playlist'].delete()
            except:
                pass
        Config.msg['playlist'] = await message.reply_text(
            pl,
            disable_web_page_preview=True,
        )
        await delete(message)


@Client.on_message(filters.command(["skip", f"skip@{Config.BOT_USERNAME}"]) & admin_filter & (filters.chat(Config.CHAT_ID) | filters.private | filters.chat(Config.LOG_GROUP)))
async def skip_track(_, m: Message):
    if not Config.playlist:
        k=await m.reply_text("⛔️ **Empty Playlist !**")
        await delete(k)
        return
    if len(m.command) == 1:
        await skip()
        await delete(m)
    else:
        try:
            items = list(dict.fromkeys(m.command[1:]))
            items = [int(x) for x in items if x.isdigit()]
            items.sort(reverse=True)
            for i in items:
                if 2 <= i <= (len(Config.playlist) - 1):
                    Config.playlist.pop(i)
                    k=await m.reply_text(f"⏭ **Succesfully Skipped !** \n{i}. **{Config.playlist[i][1]}**")
                    await delete(k)
                else:
                    k=await m.reply_text(f"⛔️ **Can't Skip First Two Video - {i} !**")
                    await delete(k)
        except (ValueError, TypeError):
            k=await m.reply_text("⛔️ **Invalid Input !**")
            await delete(k)
    pl=await get_playlist_str()
    if m.chat.type == "private":
        await m.reply_photo(photo=Config.THUMB_LINK, caption=pl, reply_markup=await get_buttons())
    elif not Config.LOG_GROUP and m.chat.type == "supergroup":
        await m.reply_photo(photo=Config.THUMB_LINK, caption=pl, reply_markup=await get_buttons())


@Client.on_message(filters.command(["pause", f"pause@{Config.BOT_USERNAME}"]) & admin_filter & (filters.chat(Config.CHAT_ID) | filters.private | filters.chat(Config.LOG_GROUP)))
async def pause_playing(_, m: Message):
    if Config.PAUSE:
        k=await m.reply_text("⏸ **Already Paused !**")
        await delete(k)
        return
    if not Config.CALL_STATUS:
        k=await m.reply_text("🤖 **Didn't Joined Video Chat !**")
        await delete(k)
        return
    await pause()
    k=await m.reply_text("⏸ **Paused Streaming !**")
    await delete(k)
    

@Client.on_message(filters.command(["resume", f"resume@{Config.BOT_USERNAME}"]) & admin_filter & (filters.chat(Config.CHAT_ID) | filters.private | filters.chat(Config.LOG_GROUP)))
async def resume_playing(_, m: Message):
    if not Config.PAUSE:
        k=await m.reply_text("▶️ **Already Playing !**")
        await delete(k)
        return
    if not Config.CALL_STATUS:
        k=await m.reply_text("🤖 **Didn't Joined Video Chat !**")
        await delete(k)
        return
    await resume()
    k=await m.reply_text("▶️ **Resumed Streaming !**")
    await delete(k)


@Client.on_message(filters.command(["volume", f"volume@{Config.BOT_USERNAME}"]) & admin_filter & (filters.chat(Config.CHAT_ID) | filters.private | filters.chat(Config.LOG_GROUP)))
async def set_vol(_, m: Message):
    if not Config.CALL_STATUS:
        k=await m.reply_text("🤖 **Didn't Joined Video Chat !**")
        await delete(k)
        return
    if len(m.command) < 2:
        k=await m.reply_text("🤖 **Please Pass Volume (0-200) !**")
        await delete(k)
        return
    await volume(int(m.command[1]))
    k=await m.reply_text(f"🔉 **Volume Set To {m.command[1]} !**")
    await delete(k)
    

@Client.on_message(filters.command(["replay", f"replay@{Config.BOT_USERNAME}"]) & admin_filter & (filters.chat(Config.CHAT_ID) | filters.private | filters.chat(Config.LOG_GROUP)))
async def replay_playout(client, m: Message):
    if not Config.CALL_STATUS:
        k=await m.reply_text("🤖 **Didn't Joined Video Chat !**")
        await delete(k)
        return
    await restart_playout()
    k=await m.reply_text("🔂 **Replaying Stream !**")
    await delete(k)


@Client.on_message(filters.command(["mute", f"mute@{Config.BOT_USERNAME}"]) & admin_filter & (filters.chat(Config.CHAT_ID) | filters.private | filters.chat(Config.LOG_GROUP)))
async def set_mute(_, m: Message):
    if not Config.CALL_STATUS:
        k=await m.reply_text("🤖 **Didn't Joined Video Chat !**")
        await delete(k)
        return
    if Config.MUTED:
        k=await m.reply_text("🔇 **Already Muted !**")
        await delete(k)
        return
    k=await mute()
    if k:
        s=await m.reply_text(f"🔇 **Succesfully Muted !**")
        await delete(s)
    else:
        s=await m.reply_text("🔇 **Already Muted !**")
        await delete(s)

@Client.on_message(filters.command(["unmute", f"unmute@{Config.BOT_USERNAME}"]) & admin_filter & (filters.chat(Config.CHAT_ID) | filters.private | filters.chat(Config.LOG_GROUP)))
async def set_unmute(_, m: Message):
    if not Config.CALL_STATUS:
        k=await m.reply_text("🤖 **Didn't Joined Video Chat !**")
        await delete(k)
        return
    if not Config.MUTED:
        k=await m.reply_text("🔊 **Already Unmuted !**")
        await delete(k)
        return
    k=await unmute()
    if k:
        s=await m.reply_text(f"🔊 **Succesfully Unmuted !**")
        await delete(s)
    else:
        s=await m.reply_text("🔊 **Already Unmuted !**")
        await delete(s)


@Client.on_message(filters.command(["current", f"current@{Config.BOT_USERNAME}"]) & (filters.chat(Config.CHAT_ID) | filters.private | filters.chat(Config.LOG_GROUP)))
async def show_current(client, m: Message):
    data=Config.DATA.get('FILE_DATA')
    if not data.get('dur', 0) or \
        data.get('dur') == 0:
        title="▶️ <b>Streaming [Live Stream](https://t.me/AsmSafone) !</b>"
    else:
        if Config.playlist:
            title=f"▶️ <b>{Config.playlist[0][1]}</b>"
        elif Config.STREAM_LINK:
            title=f"▶️ <b>Streaming [Stream Link]({data['file']}) !</b>"
        else:
            title=f"▶️ <b>Streaming [Startup Stream]({Config.STREAM_URL}) !</b>"
    if m.chat.type == "private":
        await m.reply_photo(
            photo=Config.THUMB_LINK,
            caption=title,
            reply_markup=await get_buttons()
        )
    else:
        if Config.msg.get('current') is not None:
            try:
                await Config.msg['current'].delete()
            except:
                pass
        Config.msg['current'] = await m.reply_photo(
            photo=Config.THUMB_LINK,
            caption=title,
            reply_markup=await get_buttons()
        )
        await delete(m)


@Client.on_message(filters.command(["seek", f"seek@{Config.BOT_USERNAME}"]) & admin_filter & (filters.chat(Config.CHAT_ID) | filters.private | filters.chat(Config.LOG_GROUP)))
async def seek_playout(client, m: Message):
    if not Config.CALL_STATUS:
        k=await m.reply_text("🤖 **Didn't Joined Video Chat !**")
        await delete(k)
        return
    if not (Config.playlist or Config.STREAM_LINK):
        k=await m.reply_text("⚠️ **Startup Stream Can't Be Seeked !**")
        await delete(k)
        return
    data=Config.DATA.get('FILE_DATA')
    if not data.get('dur', 0) or \
        data.get('dur') == 0:
        k=await m.reply_text("⚠️ **This Stream Can't Be Seeked !**")
        await delete(k)
        return
    if ' ' in m.text:
        i, time = m.text.split(" ")
        try:
            time=int(time)
        except:
            k=await m.reply_text("⛔️ **Invalid Time Specified !**")
            await delete(k)
            return
        k, string=await seek_file(time)
        if k == False:
            s=await m.reply_text(f"**{string}**")
            await delete(s)
            return
        if not data.get('dur', 0) or \
            data.get('dur') == 0:
            title="▶️ <b>Streaming [Live Stream](https://t.me/AsmSafone) !</b>"
        else:
            if Config.playlist:
                title=f"▶️ <b>{Config.playlist[0][1]}</b>"
            elif Config.STREAM_LINK:
                title=f"▶️ <b>Streaming [Stream Link]({data['file']}) !</b>"
            else:
                title=f"▶️ <b>Streaming [Startup Stream]({Config.STREAM_URL}) !</b>"
        s=await m.reply_text(f"{title}", reply_markup=await get_buttons(), disable_web_page_preview=True)
        await delete(s)
    else:
        s=await m.reply_text("❗ **You Should Specify The Time In Second To Seek!** \n\nFor Example: \n• `/seek 10` to foward 10 sec. \n• `/seek -10` to rewind 10 sec.")
        await delete(s)
