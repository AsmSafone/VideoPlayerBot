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
from bot.config import Config
from pyrogram import Client, filters
from pyrogram.raw import functions, types

bot = Client(
    "VideoPlayer",
    Config.API_ID,
    Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)
bot.start()
ok = bot.get_me()
USERNAME = ok.username

try:
    bot.send(
        functions.bots.SetBotCommands(
            commands=[
                types.BotCommand(
                    command="start",
                    description="Start The Bot"
                ),
                types.BotCommand(
                    command="help",
                    description="Show Help Message"
                ),
                types.BotCommand(
                    command="radio",
                    description="Start Radio Streaming"
                ),
                types.BotCommand(
                    command="stream",
                    description="Start Video Streaming"
                ),
                types.BotCommand(
                    command="endstream",
                    description="Stop Streaming & Left VC"
                ),
                types.BotCommand(
                    command="restart",
                    description="Restart The Bot (Owner Only)"
                )
            ]
        )
    )
except:
    pass
