import os
import re
import sys
import ffmpeg
import asyncio
import subprocess
from signal import SIGINT
from config import Config
from pyrogram import Client, filters
from pyrogram.types import Message
from bot.safone.player import STREAM
from bot.safone.player import ydl, group_call_factory

ADMINS = Config.ADMINS
CHAT_ID = Config.CHAT_ID
USERNAME = Config.BOT_USERNAME

RADIO_CALL = {}
FFMPEG_PROCESSES = {}


@Client.on_message(filters.command(["radio", f"radio@{USERNAME}"]) & filters.user(ADMINS) & (filters.chat(CHAT_ID) | filters.private))
async def radio(client, m: Message):
    if 1 in STREAM:
        await m.reply_text("🤖 **Please Stop The Existing Stream!**")
        return

    if not ' ' in m.text:
        await m.reply_text("❗ __Send Me An Live Radio Link / YouTube Live Video Link To Start Radio!__")
        return

    text = m.text.split(' ', 1)
    query = text[1]
    input_filename = f'radio-{CHAT_ID}.raw'
    msg = await m.reply_text("🔄 `Processing ...`")

    process = FFMPEG_PROCESSES.get(CHAT_ID)
    if process:
        try:
            process.send_signal(SIGINT)
            await asyncio.sleep(1)
        except Exception as e:
            print(e)

    regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"
    match = re.match(regex,query)
    if match:
        try:
            meta = ydl.extract_info(query, download=False)
            formats = meta.get('formats', [meta])
            for f in formats:
                ytstreamlink = f['url']
            station_stream_url = ytstreamlink
        except Exception as e:
            await msg.edit(f"❌ **YouTube Download Error!** \n\n`{e}`")
            print(e)
            return
    else:
        station_stream_url = query
        print(station_stream_url)

    process = (
        ffmpeg.input(station_stream_url)
        .output(input_filename, format='s16le', acodec='pcm_s16le', ac=2, ar='48k')
        .overwrite_output()
        .run_async()
    )
    FFMPEG_PROCESSES[CHAT_ID] = process

    if CHAT_ID in RADIO_CALL:
        await asyncio.sleep(1)
        await msg.edit(f"📻 **Started [Radio Streaming]({query})!**", disable_web_page_preview=True)
    else:
        await msg.edit("🔄 `Starting Radio Stream ...`")
        await asyncio.sleep(2)
        try:
            group_call = group_call_factory.get_file_group_call(input_filename)
            await group_call.start(CHAT_ID)
            RADIO_CALL[CHAT_ID] = group_call
            await msg.edit(f"📻 **Started [Radio Streaming]({query})!**", disable_web_page_preview=True)
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
    
        
@Client.on_message(filters.command(["stopradio", f"stopradio@{USERNAME}"]) & filters.user(ADMINS) & (filters.chat(CHAT_ID) | filters.private))
async def stopradio(client, m: Message):
    if 0 in STREAM:
        await m.reply_text("🤖 **Please Start An Stream First!**")
        return

    msg = await m.reply_text("🔄 `Processing ...`")
    process = FFMPEG_PROCESSES.get(CHAT_ID)
    if process:
        try:
            process.send_signal(SIGINT)
            await asyncio.sleep(3)
        except Exception as e:
            print(e)

    if CHAT_ID in RADIO_CALL:
        await RADIO_CALL[CHAT_ID].stop()
        RADIO_CALL.pop(CHAT_ID)
        await msg.edit("⏹️ **Stopped Radio Streaming!**")
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
