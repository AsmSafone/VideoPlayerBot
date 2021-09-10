import os
import re
import sys
import ffmpeg
import asyncio
import subprocess
from asyncio import sleep
from signal import SIGINT
from bot.config import Config, db
from pyrogram import Client, filters
from pyrogram.types import Message
from bot.safone.extras import USERNAME
from bot.safone.player import ydl, group_call_factory

ADMINS = Config.ADMINS
CHAT_ID = Config.CHAT_ID
VIDEO_CALL = db.VIDEO_CALL
RADIO_CALL = db.RADIO_CALL
FFMPEG_PROCESSES = db.FFMPEG_PROCESSES

@Client.on_message(filters.command(["radio", f"radio@{USERNAME}"]) & filters.user(ADMINS) & (filters.chat(CHAT_ID) | filters.private))
async def radio(client, m: Message):
    if not ' ' in m.text:
        await m.reply_text("❗ __Send Me An Live Radio Link / YouTube Live Video Link To Start Radio Streaming!__")
        return

    text = m.text.split(' ', 1)
    query = text[1]
    input_filename = f'radio-{CHAT_ID}.raw'
    msg = await m.reply_text("🔄 `Processing ...`")

    vid_call = VIDEO_CALL.get(CHAT_ID)
    if vid_call:
        await VIDEO_CALL[CHAT_ID].stop()
        VIDEO_CALL.pop(CHAT_ID)
        await sleep(3)

    process = FFMPEG_PROCESSES.get(CHAT_ID)
    if process:
        try:
            process.send_signal(SIGINT)
            await sleep(3)
        except Exception as e:
            print(e)
            pass

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
            await msg.edit(f"❌ **YouTube Download Error !** \n\n`{e}`")
            print(e)
            return
    else:
        station_stream_url = query
        print(station_stream_url)

    if os.path.exists(input_filename):
        os.remove(input_filename)

    process = (
        ffmpeg.input(station_stream_url)
        .output(input_filename, format='s16le', acodec='pcm_s16le', ac=2, ar='48k')
        .overwrite_output()
        .run_async()
    )
    FFMPEG_PROCESSES[CHAT_ID] = process

    if CHAT_ID in RADIO_CALL:
        await sleep(1)
        await msg.edit(f"📻 **Started [Radio Streaming]({query}) !**", disable_web_page_preview=True)
    else:
        await msg.edit("🔄 `Starting Radio Stream ...`")
        await sleep(2)
        group_call = group_call_factory.get_file_group_call(input_filename)
        try:
            await group_call.start(CHAT_ID)
            RADIO_CALL[CHAT_ID] = group_call
            await msg.edit(f"📻 **Started [Radio Streaming]({query}) !**", disable_web_page_preview=True)
        except Exception as e:
            await msg.edit(f"❌ **An Error Occoured !** \n\nError: `{e}`")


@Client.on_message(filters.command(["restart", f"restart@{USERNAME}"]) & filters.user(ADMINS) & (filters.chat(CHAT_ID) | filters.private))
async def restart(client, m: Message):
    k = await m.reply_text("🔄 `Restarting ...`")
    await sleep(3)
    process = FFMPEG_PROCESSES.get(CHAT_ID)
    if process:
        try:
            process.send_signal(SIGINT)
            await sleep(3)
        except subprocess.TimeoutExpired:
            process.kill()
        except Exception as e:
            print(e)
            pass
        FFMPEG_PROCESSES[CHAT_ID] = ""
    os.execl(sys.executable, sys.executable, *sys.argv)
    try:
        await k.edit("✅ **Restarted Successfully! \nJoin @AsmSafone For More!**")
    except:
        pass
