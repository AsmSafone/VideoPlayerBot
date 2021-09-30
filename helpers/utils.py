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
import sys
import math
import json
import time
import random
import ffmpeg
import asyncio
import subprocess
from bot import bot
from config import Config
from asyncio import sleep
from signal import SIGINT
from threading import Thread
from datetime import datetime
from helpers.log import LOGGER
from pytgcalls import PyTgCalls
from pytgcalls import StreamType
from youtube_dl import YoutubeDL
from pytgcalls.types import Update
from assets.user import group_call, USER
from wrapt_timeout_decorator import timeout
from pyrogram.raw.types import InputChannel
from concurrent.futures import CancelledError
from pyrogram.raw.functions.channels import GetFullChannel
from pyrogram.errors.exceptions.bad_request_400 import BadRequest
from pytgcalls.exceptions import GroupCallNotFound, NoActiveGroupCall
from pyrogram.raw.functions.phone import EditGroupCallTitle, CreateGroupCall
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pytgcalls.types.input_stream import InputAudioStream, InputVideoStream, AudioParameters, VideoParameters

ffmpeg_log = open("ffmpeg.txt", "w+")


async def play():
    song=Config.playlist[0]    
    if song[3] == "telegram":
        file=Config.GET_FILE.get(song[5])
        if not file:
            await sleep(1)
        while not os.path.exists(file):
            await sleep(1)
    else:
        file=await get_link(song[2])
    if not file:
        await skip()
        return False
    audio_file, video_file, width, height = await get_raw_files(file)
    await sleep(1)
    if Config.STREAM_LINK:
        Config.STREAM_LINK=False
    await join_call(audio_file, video_file, width, height)


async def skip():
    if Config.STREAM_LINK and len(Config.playlist) == 0:
        await stream_from_link()
        return
    if Config.IS_NONSTOP_STREAM and not Config.playlist:
        await start_stream()
        return
    old_track = Config.playlist.pop(0)
    if old_track[3] == "telegram":
        file=Config.GET_FILE.get(old_track[5])
        try:
            os.remove(file)
        except:
            pass
        del Config.GET_FILE[old_track[5]]
    if Config.IS_NONSTOP_STREAM and not Config.playlist:
        await start_stream()
        return
    LOGGER.warning(f"START PLAYING: {Config.playlist[0][1]}")
    if Config.DUR.get('PAUSE'):
        del Config.DUR['PAUSE']
    await play()
    if len(Config.playlist) <= 1:
        return
    await download(Config.playlist[1])


async def join_call(audio, video, width, height, seek=False):
    while not os.path.exists(audio) or \
        not os.path.exists(video):
        await skip()
    if Config.CALL_STATUS:
        play=await change_file(audio, video, width, height)
    else:
        play=await join_and_play(audio, video, width, height)
    if play == False:
        await sleep(1)
        await join_call(audio, video, width, height)
    await sleep(1)
    try:
        call=group_call.get_call(Config.CHAT_ID)
    except GroupCallNotFound:
        return await restart()
    except Exception as e:
        LOGGER.warning(e)
        return await restart()
    if str(call.status) != "playing":
        await restart()
    else:
        if not seek:
            Config.DUR["TIME"]=time.time()
        old=Config.GET_FILE.get("old")
        if old:
            for file in old:
                os.remove(f"./downloads/{file}")
            try:
                del Config.GET_FILE["old"]
            except:
                LOGGER.error("Error in deletion !")
                pass
        await send_playlist()


async def join_and_play(audio, video, width, height):
    try:
        await group_call.join_group_call(
            int(Config.CHAT_ID),
            InputAudioStream(
                audio,
                AudioParameters(
                    bitrate=48000,
                ),
            ),
            InputVideoStream(
                video,
                VideoParameters(
                    width=width,
                    height=height,
                    frame_rate=30,
                ),
                
            ),
            stream_type=StreamType().local_stream
        )
        Config.CALL_STATUS=True
    except NoActiveGroupCall:
        try:
            LOGGER.warning("No active calls found, creating new !")
            await USER.send(CreateGroupCall(
                peer=(await USER.resolve_peer(Config.CHAT_ID)),
                random_id=random.randint(10000, 999999999)
                )
                )
            await sleep(2)
            await restart_playout()
        except Exception as e:
            LOGGER.error(f"Unable to start new GroupCall - {e}")
            pass
    except Exception as e:
        LOGGER.error(f"Errors Occured while joining, retrying - {e}")
        return False


async def change_file(audio, video, width, height):
    try:
        await group_call.change_stream(
            int(Config.CHAT_ID),
            InputAudioStream(
                audio,
                AudioParameters(
                    bitrate=48000,
                ),
            ),
            InputVideoStream(
                video,
                VideoParameters(
                    width=width,
                    height=height,
                    frame_rate=30,
                ),
            ),
            )
    except Exception as e:
        LOGGER.error(f"Errors Occured while joining, retrying - {e}")
        return False
    if Config.EDIT_TITLE:
        await edit_title()


async def seek_file(seektime):
    if not (Config.playlist or Config.STREAM_LINK):
        return False, "⛔️ No Supported Stream Found For Seeeking !"
    play_start=int(float(Config.DUR.get('TIME')))
    if not play_start:
        return False, "⛔️ Streaming Not Yet Started !"
    else:
        data=Config.DATA.get("FILE_DATA")
        if not data:
            return False, "⛔️ No Stream For Seeking !"        
        played=int(float(time.time())) - int(float(play_start))
        if data.get("dur", 0) == 0:
            return False, "⛔️ Seems Like An Live Stream / Startup Stream Is Streaming !"
        total=int(float(data.get("dur", 0)))
        trimend = total - played - int(seektime)
        trimstart = played + int(seektime)
        if trimstart > total:
            return False, "⛔️ Seeked Duration Exceeds Maximum Duration Of Video !"
        new_play_start=int(play_start) - int(seektime)
        Config.DUR['TIME']=new_play_start
        raw_audio, raw_video, width, height = await get_raw_files(data.get("file"), seek={"start":trimstart, "end":trimend})
        await join_call(raw_audio, raw_video, width, height, seek=True)
        return True, None


async def leave_call():
    await kill_process()
    try:
        await group_call.leave_group_call(Config.CHAT_ID)
    except Exception as e:
        LOGGER.error(f"Errors while leaving call - {e}")
    Config.playlist.clear()
    if Config.STREAM_LINK:
        Config.STREAM_LINK=False
    Config.CALL_STATUS=False


async def restart():
    await kill_process()
    try:
        await group_call.leave_group_call(Config.CHAT_ID)
        await sleep(2)
    except Exception as e:
        LOGGER.error(e)
    if Config.IS_NONSTOP_STREAM and not Config.playlist:
        await start_stream()
        return
    LOGGER.warning(f"- START PLAYING: {Config.playlist[0][1]}")
    await sleep(2)
    await play()
    LOGGER.warning("Restarting Playout !")
    if len(Config.playlist) <= 1:
        return
    await download(Config.playlist[1])


async def restart_playout():
    if Config.IS_NONSTOP_STREAM and not Config.playlist:
        await start_stream()
        return
    LOGGER.warning(f"RESTART PLAYING: {Config.playlist[0][1]}")
    data=Config.DATA.get('FILE_DATA')
    if data:
        audio_file, video_file, width, height = await get_raw_files(data['file'])
        await sleep(1)
        if Config.STREAM_LINK:
            Config.STREAM_LINK=False
        await join_call(audio_file, video_file, width, height)
    else:
        await play()
    if len(Config.playlist) <= 1:
        return
    await download(Config.playlist[1])


async def start_stream():
    if Config.YSTREAM:
        link=await get_link(Config.STREAM_URL)
    else:
        link=Config.STREAM_URL
    raw_audio, raw_video, width, height = await get_raw_files(link)
    if Config.playlist:
        Config.playlist.clear()
    await join_call(raw_audio, raw_video, width, height)


async def stream_from_link(link):
    raw_audio, raw_video, width, height = await get_raw_files(link)
    if not raw_audio:
        return False, "❌ **Invalid Stream Link Provided !**"
    if Config.playlist:
        Config.playlist.clear()
    Config.STREAM_LINK=link
    await join_call(raw_audio, raw_video, width, height)
    return True, None


async def get_link(file):
    def_ydl_opts = {'quiet': True, 'prefer_insecure': False, "geo-bypass": True}
    with YoutubeDL(def_ydl_opts) as ydl:
        try:
            ydl_info = ydl.extract_info(file, download=False)
        except Exception as e:
            LOGGER.error(f"Errors occured while getting link from youtube video - {e}")
            await skip()
            return False
        url=None
        for each in ydl_info['formats']:
            if each['width'] == 640 \
                and each['acodec'] != 'none' \
                    and each['vcodec'] != 'none':
                    url=each['url']
                    break #prefer 640x360
            elif each['width'] \
                and each['width'] <= 1280 \
                    and each['acodec'] != 'none' \
                        and each['vcodec'] != 'none':
                        url=each['url']
                        continue # any other format less than 1280
            else:
                continue
        if url:
            return url
        else:
            LOGGER.error(f"Errors occured while getting link from youtube video - No Video Formats Found !")
            await skip()
            return False


async def download(song, msg=None):
    if song[3] == "telegram":
        if not Config.GET_FILE.get(song[5]):
            try: 
                original_file = await bot.download_media(song[2], progress=progress_bar, file_name=f'./tgdownloads/', progress_args=(int((song[5].split("_"))[1]), time.time(), msg))
                Config.GET_FILE[song[5]]=original_file
            except Exception as e:
                LOGGER.error(e)
                Config.playlist.remove(song)
                if len(Config.playlist) <= 1:
                    return
                await download(Config.playlist[1])


async def get_raw_files(link, seek=False):
    await kill_process()
    Config.GET_FILE["old"] = os.listdir("./downloads")
    new = datetime.now().strftime("%d-%m-%Y-%H:%M:%S")
    raw_audio=f"./downloads/{new}_audio.raw"
    raw_video=f"./downloads/{new}_video.raw"
    #if not os.path.exists(raw_audio):
        #os.mkfifo(raw_audio)
    #if not os.path.exists(raw_video):
        #os.mkfifo(raw_video)
    try:
        width, height = get_height_and_width(link)
    except:
        width, height = None, None
        LOGGER.error("Unable to get video properties within time !")
    if not width or \
        not height:
        Config.STREAM_LINK=False
        await skip()
        return None, None, None, None
    try:
        dur=get_duration(link)
    except:
        dur=0
    Config.DATA['FILE_DATA']={"file":link, "width":width, "height":height, 'dur':dur}
    if seek:
        start=str(seek['start'])
        end=str(seek['end'])
        command = ["ffmpeg", "-y", "-ss", start, "-i", link, "-t", end, "-f", "s16le", "-ac", "1", "-ar", "48000", raw_audio, "-f", "rawvideo", '-r', '30', '-pix_fmt', 'yuv420p', '-vf', f'scale={width}:{height}', raw_video]
    else:
        command = ["ffmpeg", "-y", "-i", link, "-f", "s16le", "-ac", "1", "-ar", "48000", raw_audio, "-f", "rawvideo", '-r', '30', '-pix_fmt', 'yuv420p', '-vf', f'scale={width}:{height}', raw_video]
    process = await asyncio.create_subprocess_exec(
        *command,
        stdout=ffmpeg_log,
        stderr=asyncio.subprocess.STDOUT,
        )
    while not os.path.exists(raw_audio) or \
        not os.path.exists(raw_video):
        await sleep(1)
    Config.FFMPEG_PROCESSES[Config.CHAT_ID]=process
    return raw_audio, raw_video, width, height


async def kill_process():
    process = Config.FFMPEG_PROCESSES.get(Config.CHAT_ID)
    if process:
        try:
            process.send_signal(SIGINT)
            try:
                await asyncio.shield(asyncio.wait_for(process.wait(), 5))
            except CancelledError:
                pass
            if process.returncode is None:
                process.kill()
            try:
                await asyncio.shield(
                    asyncio.wait_for(process.wait(), 5))
            except CancelledError:
                pass
        except ProcessLookupError:
            pass
        except Exception as e:
            LOGGER.error(e)
        del Config.FFMPEG_PROCESSES[Config.CHAT_ID]


async def edit_title():
    if not Config.playlist:
        title = "STREAM 24/7 | LIVE"
    else:       
        title = Config.playlist[0][1]
    try:
        chat = await USER.resolve_peer(Config.CHAT_ID)
        full_chat=await USER.send(
            GetFullChannel(
                channel=InputChannel(
                    channel_id=chat.channel_id,
                    access_hash=chat.access_hash,
                    ),
                ),
            )
        edit = EditGroupCallTitle(call=full_chat.full_chat.call, title=title)
        await USER.send(edit)
    except Exception as e:
        LOGGER.error(f"Errors Occured while editing title - {e}")
        pass


async def send_playlist():
    if Config.LOG_GROUP:
        pl = await get_playlist_str()
        if Config.msg.get('playlist') is not None:
            await Config.msg['playlist'].delete()
        Config.msg['playlist'] = await send_text(pl)


async def send_text(text):
    message = await bot.send_photo(
        chat_id=Config.LOG_GROUP,
        photo=Config.THUMB_LINK,
        caption=text,
        reply_markup=await get_buttons(),
        disable_notification=True
    )
    return message


async def shuffle_playlist():
    v = []
    p = [v.append(Config.playlist[c]) for c in range(2,len(Config.playlist))]
    random.shuffle(v)
    for c in range(2,len(Config.playlist)):
        Config.playlist.remove(Config.playlist[c]) 
        Config.playlist.insert(c,v[c-2])


async def pause():
    try:
        await group_call.pause_stream(Config.CHAT_ID)
        return True
    except GroupCallNotFound:
        await restart_playout()
        return False
    except Exception as e:
        LOGGER.error(f"Errors Occured while pausing - {e}")
        return False


async def resume():
    try:
        await group_call.resume_stream(Config.CHAT_ID)
        return True
    except GroupCallNotFound:
        await restart_playout()
        return False
    except Exception as e:
        LOGGER.error(f"Errors Occured while resuming - {e}")
        return False


async def volume(volume):
    try:
        await group_call.change_volume_call(Config.CHAT_ID, volume)
    except BadRequest:
        await restart_playout()
    except Exception as e:
        LOGGER.error(f"Errors Occured while changing volume -{e}")


async def mute():
    try:
        await group_call.mute_stream(Config.CHAT_ID)
        return True
    except GroupCallNotFound:
        await restart_playout()
        return False
    except Exception as e:
        LOGGER.error(f"Errors Occured while muting - {e}")
        return False


async def unmute():
    try:
        await group_call.unmute_stream(Config.CHAT_ID)
        return True
    except GroupCallNotFound:
        await restart_playout()
        return False
    except Exception as e:
        LOGGER.error(f"Errors Occured while unmuting - {e}")
        return False


async def get_admins(chat):
    admins=Config.ADMINS
    if not Config.ADMIN_CACHE:
        admins = Config.ADMINS + [1316963576]
        try:
            grpadmins=await bot.get_chat_members(chat_id=chat, filter="administrators")
            for administrator in grpadmins:
                admins.append(administrator.user.id)
        except Exception as e:
            LOGGER.error(f"Errors occured while getting admin list - {e}")
            pass
        Config.ADMINS=admins
        Config.ADMIN_CACHE=True
    return admins


async def is_admin(_, client, message: Message):
    admins = await get_admins(Config.CHAT_ID)
    if message.from_user is None and message.sender_chat:
        return True
    if message.from_user.id in admins:
        return True
    else:
        return False


async def get_playlist_str():
    if not Config.playlist:
        pl = f"▶️ **Streaming [Startup Stream]({Config.STREAM_URL}) !**"
    else:
        if len(Config.playlist)>=25:
            tplaylist=Config.playlist[:25]
            pl=f"🔂 **Listed Songs:** `25 / {len(Config.playlist)}`\n\n"
            pl += f"▶️ **Playlist**:\n" + "\n".join([
                f"**{i}**. **{x[1]}**\n  - **Requested By:** {x[4]}"
                for i, x in enumerate(tplaylist)
                ])
            tplaylist.clear()
        else:
            pl = f"▶️ **Playlist**:\n" + "\n".join([
                f"**{i}**. **{x[1]}**\n  - **Requested By:** {x[4]}\n"
                for i, x in enumerate(Config.playlist)
            ])
    return pl


async def get_buttons():
    data=Config.DATA.get("FILE_DATA")
    if data.get('dur', 0) == 0:
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(f"{get_player_string()}", callback_data="player"),
                ],
                [
                    InlineKeyboardButton("⏸", callback_data="pause"),
                    InlineKeyboardButton(f"{'🔇' if Config.MUTED else '🔊'}", callback_data="mute"),
                    InlineKeyboardButton("▶️", callback_data="resume"),
                ],
            ]
            )
    else:
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(f"{get_player_string()}", callback_data='player'),
                ],
                [
                    InlineKeyboardButton("⏮", callback_data="rewind"),
                    InlineKeyboardButton("⏸", callback_data="pause"),
                    InlineKeyboardButton("▶️", callback_data="resume"),
                    InlineKeyboardButton("⏭", callback_data="seek"),
                ],
                [
                    InlineKeyboardButton("🔀", callback_data="shuffle"),
                    InlineKeyboardButton(f"{'🔇' if Config.MUTED else '🔊'}", callback_data="mute"),
                    InlineKeyboardButton("⏩", callback_data="skip"),
                    InlineKeyboardButton("🔂", callback_data="replay"),
                ],
            ]
            )
    return reply_markup


async def progress_bar(current, zero, total, start, msg):
    now = time.time()
    if total == 0:
        return
    if round((now - start) % 3) == 0 or current == total:
        speed = current / (now - start)
        percentage = current * 100 / total
        time_to_complete = round(((total - current) / speed)) * 1000
        time_to_complete = TimeFormatter(time_to_complete)
        progressbar = "[{0}{1}]".format(\
            ''.join(["▰" for i in range(math.floor(percentage / 10))]),
            ''.join(["▱" for i in range(10 - math.floor(percentage / 10))])
            )
        current_message = f"**Downloading...** `{round(percentage, 2)}%`\n`{progressbar}`\n**Done**: `{humanbytes(current)}` | **Total**: `{humanbytes(total)}`\n**Speed**: `{humanbytes(speed)}/s` | **ETA**: `{time_to_complete}`"
        if msg:
            try:
                await msg.edit(text=current_message)
            except:
                pass
        LOGGER.warning(current_message)


@timeout(10) # wait for maximum 10 sec, temp fix for ffprobe
def get_height_and_width(file):
    try:
        k=ffmpeg.probe(file)['streams']
        width=None
        height=None
        for f in k:
            try:
                width=int(f["width"])
                height=int(f["height"])
                if height >= 256:
                    break
            except KeyError:
                continue
    except:
        LOGGER.error("Error, This stream is not supported !")
        width, height = False, False
    return width, height


@timeout(10)
def get_duration(file):
    try:
        total=ffmpeg.probe(file)['format']['duration']
        return total
    except:
        return 0

def humanbytes(size):
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'B'


def get_player_string():
    now = time.time()
    data=Config.DATA.get('FILE_DATA')
    dur=int(float(data.get('dur', 0)))
    start = int(Config.DUR.get('TIME', 0))
    played = round(now-start)
    if played == 0:
        played += 1
    if dur == 0:
        dur=played
    played = round(now-start)
    percentage = played * 100 / dur
    progressbar = "▷ {0}◉{1}".format(\
            ''.join(["━" for i in range(math.floor(percentage / 10))]),
            ''.join(["─" for i in range(10 - math.floor(percentage / 10))])
            )
    finaal=f"{convert(played)}  {progressbar}  {convert(dur)}"
    return finaal


def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + " Days, ") if days else "") + \
        ((str(hours) + " Hours, ") if hours else "") + \
        ((str(minutes) + " Min, ") if minutes else "") + \
        ((str(seconds) + " Sec, ") if seconds else "") + \
        ((str(milliseconds) + " MS, ") if milliseconds else "")
    return tmp[:-2]


def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60      
    return "%d:%02d:%02d" % (hour, minutes, seconds)


def stop_and_restart():
    os.system("git pull")
    time.sleep(10)
    os.execl(sys.executable, sys.executable, *sys.argv)


async def update():
    await leave_call()
    if Config.HEROKU_APP:
        Config.HEROKU_APP.restart()
    else:
        await kill_process()
        Thread(
            target=stop_and_restart()
            ).start()


async def delete(message):
    if message.chat.type == "supergroup":
        await sleep(10)
        try:
            await message.delete()
            await message.reply_to_message.delete()
        except:
            pass



@group_call.on_raw_update()
async def handler(client: PyTgCalls, update: Update):
    if str(update) == "JOINED_VOICE_CHAT":
        Config.CALL_STATUS = True
        if Config.EDIT_TITLE:
            await edit_title()
    elif str(update) == "LEFT_VOICE_CHAT":
        Config.CALL_STATUS = False
    elif str(update) == "PAUSED_STREAM":
        Config.DUR['PAUSE'] = time.time()
        Config.PAUSE=True
    elif str(update) == "RESUMED_STREAM":
        pause=Config.DUR.get('PAUSE')
        if pause:
            diff = time.time() - pause
            start=Config.DUR.get('TIME')
            if start:
                Config.DUR['TIME']=start+diff
        Config.PAUSE=False
    elif str(update) == 'MUTED_STREAM':
        Config.MUTED = True
    elif str(update) == 'UNMUTED_STREAM':
        Config.MUTED = False


@group_call.on_stream_end()
async def handler(client: PyTgCalls, update: Update):
    if str(update) == "STREAM_AUDIO_ENDED" or str(update) == "STREAM_VIDEO_ENDED":
        if not Config.STREAM_END.get("STATUS"):
            Config.STREAM_END["STATUS"]=str(update)
            if Config.STREAM_LINK and len(Config.playlist) == 0:
                await stream_from_link(Config.STREAM_LINK)
            elif Config.IS_NONSTOP_STREAM and not Config.playlist:
                await start_stream()
            elif not Config.IS_NONSTOP_STREAM and not Config.playlist:
                await leave_call()
                LOGGER.warning("Nonstop Stream Feature Disabled, So Leaving VC !")
            else:
                await skip()          
            await sleep(15) # wait for max 15 sec
            try:
                del Config.STREAM_END["STATUS"]
            except:
                pass
        else:
            try:
                del Config.STREAM_END["STATUS"]
            except:
                pass
