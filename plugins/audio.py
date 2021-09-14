import os
import re
import sys
import ffmpeg
import asyncio
import subprocess
from asyncio import sleep
from pyrogram import Client, filters
from pyrogram.types import Message
from helper.bot_utils import USERNAME
from config import AUDIO_CALL, VIDEO_CALL
from plugins.video import ydl, group_call
from helper.decorators import authorized_users_only, sudo_users_only
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


@Client.on_message(filters.command(["play", f"play@{USERNAME}"]) & filters.group & ~filters.edited)
@authorized_users_only
async def play(client, m: Message):
    media = m.reply_to_message
    if not media and not ' ' in m.text:
        await m.reply_text(
            "💁🏻‍♂️ Do you want to search for a YouTube video?",
            reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "✅ Yes", switch_inline_query_current_chat=""
                    ),
                    InlineKeyboardButton(
                        "No ❌", callback_data="close"
                    )
                ]
            ]
        )
    )

    elif ' ' in m.text:
        text = m.text.split(' ', 1)
        query = text[1]
        chat_id = m.chat.id
        msg = await m.reply_text("🔄 `Processing ...`")

        vid_call = VIDEO_CALL.get(chat_id)
        if vid_call:
            await VIDEO_CALL[chat_id].stop()
            VIDEO_CALL.pop(chat_id)
            await sleep(3)

        aud_call = AUDIO_CALL.get(chat_id)
        if aud_call:
            await AUDIO_CALL[chat_id].stop()
            AUDIO_CALL.pop(chat_id)
            await sleep(3)

        regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"
        match = re.match(regex,query)
        if match:
            await msg.edit("🔄 `Starting YouTube Audio Stream ...`")
            try:
                meta = ydl.extract_info(query, download=False)
                formats = meta.get('formats', [meta])
                for f in formats:
                        ytstreamlink = f['url']
                ytstream = ytstreamlink
            except Exception as e:
                await msg.edit(f"❌ **YouTube Download Error !** \n\n`{e}`")
                print(e)
                return
            await sleep(2)
            try:
                await group_call.join(chat_id)
                await group_call.start_audio(ytstream, repeat=False)
                AUDIO_CALL[chat_id] = group_call
                await msg.edit(f"▶️ **Started [YouTube Audio Streaming]({query}) !**", disable_web_page_preview=True)
            except Exception as e:
                await msg.edit(f"❌ **An Error Occoured!** \n\nError: `{e}`")
        else:
            await msg.edit("🔄 `Starting Live Audio Stream ...`")
            livestream = query
            await sleep(2)
            try:
                await group_call.join(chat_id)
                await group_call.start_audio(livestream, repeat=False)
                AUDIO_CALL[chat_id] = group_call
                await msg.edit(f"▶️ **Started [Live Audio Streaming]({query}) !**", disable_web_page_preview=True)
            except Exception as e:
                await msg.edit(f"❌ **An Error Occoured !** \n\nError: `{e}`")

    elif media.audio or media.document:
        chat_id = m.chat.id
        msg = await m.reply_text("🔄 `Downloading ...`")
        audio = await client.download_media(media)
        await msg.edit("🔄 `Processing ...`")
        await sleep(2)

        vid_call = VIDEO_CALL.get(chat_id)
        if vid_call:
            await VIDEO_CALL[chat_id].stop()
            VIDEO_CALL.pop(chat_id)
            await sleep(3)

        aud_call = AUDIO_CALL.get(chat_id)
        if aud_call:
            await AUDIO_CALL[chat_id].stop()
            AUDIO_CALL.pop(chat_id)
            await sleep(3)

        try:
            await group_call.join(chat_id)
            await group_call.start_audio(audio, repeat=False)
            AUDIO_CALL[chat_id] = group_call
            await msg.edit(f"▶️ **Started [Audio Streaming](https://t.me/AsmSafone) !**", disable_web_page_preview=True)
        except Exception as e:
            await msg.edit(f"❌ **An Error Occoured !** \n\nError: `{e}`")

    else:
        await m.reply_text("❗ __Send Me An Live Stream Link / YouTube Video Link / Reply To An Audio To Start Audio Streaming!__")


@Client.on_message(filters.command(["restart", f"restart@{USERNAME}"]))
@sudo_users_only
async def restart(client, m: Message):
    k = await m.reply_text("🔄 `Restarting ...`")
    await sleep(3)
    os.execl(sys.executable, sys.executable, *sys.argv)
    try:
        await k.edit("✅ **Restarted Successfully! \nJoin @AsmSafone For More!**")
    except:
        pass
