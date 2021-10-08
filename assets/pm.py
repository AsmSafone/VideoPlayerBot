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

from config import Config
from helpers.log import LOGGER
from pyrogram import Client, filters
from pyrogram.errors import BotInlineDisabled

async def is_reply(_, client, message):
    if Config.REPLY_MESSAGE:
        return True
    else:
        return False

reply_filter=filters.create(is_reply)

@Client.on_message(reply_filter & filters.private & filters.incoming & ~filters.bot & ~filters.service & ~filters.me & ~filters.chat([777000, 454000]))
async def nopm(client, message):
    try:
        inline = await client.get_inline_bot_results(Config.BOT_USERNAME, "SAF_ONE")
        m=await client.send_inline_bot_result(
            message.chat.id,
            query_id=inline.query_id,
            result_id=inline.results[0].id,
            hide_via=True
            )
        old=Config.msg.get(message.chat.id)
        if old:
            await client.delete_messages(message.chat.id, [old["msg"], old["s"]])
        Config.msg[message.chat.id]={"msg":m.updates[1].message.id, "s":message.message_id}
    except BotInlineDisabled:
        LOGGER.error(f"Inline Mode for @{Config.BOT_USERNAME} is not enabled. Enable from @Botfather to enable PM Permit !")
        await message.reply_text(f"{Config.REPLY_MESSAGE}\n\n<b>© Powered By : \n@AsmSafone | @AsmSupport 👑</b>")
    except Exception as e:
        LOGGER.error(e)
        pass
