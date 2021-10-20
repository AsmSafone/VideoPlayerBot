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
from pyrogram import Client, filters
from helpers.bot_utils import USERNAME
from pyrogram.errors import BotInlineDisabled
from config import API_ID, API_HASH, SESSION_STRING, REPLY_MESSAGE, OLD_PMS

User = Client(
    SESSION_STRING,
    API_ID,
    API_HASH
)


@User.on_message(filters.private & filters.incoming & ~filters.bot & ~filters.service & ~filters.me & ~filters.edited & ~filters.chat([777000, 454000]))
async def nopm(client, message):
    if REPLY_MESSAGE is not None:
        try:
            inline = await client.get_inline_bot_results(USERNAME, "SAF_ONE")
            m = await client.send_inline_bot_result(
                message.chat.id,
                query_id=inline.query_id,
                result_id=inline.results[0].id,
                hide_via=True
                )
            old = OLD_PMS.get(message.chat.id)
            if old:
                await client.delete_messages(message.chat.id, [old["msg"], old["s"]])
            OLD_PMS[message.chat.id] = {"msg":m.updates[1].message.id, "s":message.message_id}
        except BotInlineDisabled:
            print(f"[WARN] - Inline Mode for @{USERNAME} is not enabled. Enable from @Botfather to enable PM Permit !")
            await message.reply_text(f"{REPLY_MESSAGE}\n\n<b>© Powered By : \n@AsmSafone | @AsmSupport 👑</b>")
        except Exception as e:
            print(e)
            pass
