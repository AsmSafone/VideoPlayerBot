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
import asyncio
from bot import bot
from config import Config
from pyrogram import idle
from helpers.log import LOGGER
from helpers.utils import start_stream
from assets.user import group_call, USER
from pyrogram.errors import UserAlreadyParticipant


if not os.path.isdir("./downloads"):
    os.makedirs("./downloads")
else:
    for f in os.listdir("./downloads"):
        os.remove(f"./downloads/{f}")

async def main():
    await bot.start()
    Config.BOT_USERNAME = (await bot.get_me()).username
    await group_call.start()
    LOGGER.warning(f"{Config.BOT_USERNAME} Started Successfully !")
    if Config.IS_NONSTOP_STREAM:
        await start_stream()
    try:
        await USER.join_chat("AsmSafone")
    except UserAlreadyParticipant:
        pass
    except Exception as e:
        print(e)
        pass
    await idle()
    LOGGER.warning("Video Player Bot Stopped !")
    await bot.stop()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())



