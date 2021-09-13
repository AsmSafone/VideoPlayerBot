import os
from config import ASSISTANT_NAME
from helper.bot_utils import BOT_NAME


START_TEXT = f"👋🏻 **Hello**, \n\nI'm **{BOT_NAME}**. \nI Can Stream Lives, Radios, YouTube Videos & Telegram Video Files On Voice Chat Of Telegram Groups. Let's Enjoy Cinematic View Of Group Video Player With Your Friends 😉! \n\n**Made With ❤️ By @ImSafone!** 👑"
HELP_TEXT = f"""
🛠 **Setting Up Bot**:

\u2022 Start Voice Chat In Your Group!
\u2022 Add Me & @{ASSISTANT_NAME} To Your Group!
\u2022 Give Admin To Me & **@{ASSISTANT_NAME}** In Your Group!

⚔️ **Available Commands**:

\u2022 `/play` - start streaming the audio
\u2022 `/stream` - start streaming the video
\u2022 `/pause` - pause the current stream
\u2022 `/resume` - resume the paused stream
\u2022 `/endstream` - stop streaming & left vc
\u2022 `/restart` - restart the bot (sudo only)

© **Powered By** : 
**@AsmSafone | @SafoTheBot** 👑
"""
ABOUT_TEXT = f"💡 **Information**: \n\nThis bot is created for streaming videos in telegram group video chats using several methods from WebRTC. Powered by pytgcalls the async client API for the Telegram Group Calls and Pyrogram the telegram MTProto API Client Library and Framework in Pure Python for Users and Bots. \n\n**This bot licensed under GNU-GPL 3.0 License!**"
