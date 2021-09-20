# Telegram Video Player Bot [![Mentioned in Awesome](https://awesome.re/mentioned-badge-flat.svg)](https://github.com/tgcalls/awesome-tgcalls)
![GitHub Repo stars](https://img.shields.io/github/stars/AsmSafone/VideoPlayerBot?color=blue&style=flat)
![GitHub forks](https://img.shields.io/github/forks/AsmSafone/VideoPlayerBot?color=green&style=flat)
![GitHub issues](https://img.shields.io/github/issues/AsmSafone/VideoPlayerBot)
![GitHub closed issues](https://img.shields.io/github/issues-closed/AsmSafone/VideoPlayerBot)
![GitHub pull requests](https://img.shields.io/github/issues-pr/AsmSafone/VideoPlayerBot)
![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed/AsmSafone/VideoPlayerBot)
![GitHub contributors](https://img.shields.io/github/contributors/AsmSafone/VideoPlayerBot?style=flat)
![GitHub repo size](https://img.shields.io/github/repo-size/AsmSafone/VideoPlayerBot?color=red)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/AsmSafone/VideoPlayerBot)
![GitHub](https://img.shields.io/github/license/AsmSafone/VideoPlayerBot)
[![Bot Updates](https://img.shields.io/badge/VideoPlayerBot-Updates%20Channel-green)](https://t.me/AsmSafone)
[![Bot Support](https://img.shields.io/badge/VideoPlayerBot-Support%20Group-blue)](https://t.me/safothebot)

An Telegram Bot By [@AsmSafone](https://t.me/AsmSafone) To Stream Videos in Telegram Voice Chat.

## Main Features

- Supports Live Streaming.
- Supports YouTube Streaming.
- Supports Live Radio Streaming.
- Supports Video Files Streaming.
- Supports YouTube Live Streaming.
- User Account Protection (PM Guard)

## Deploy Own Bot

### Railway (Recommended)
<p><a href="https://railway.app/new/template?template=https%3A%2F%2Fgithub.com%2FAsmSafone%2FVideoPlayerBot&envs=API_ID%2CAPI_HASH%2CBOT_TOKEN%2CSESSION_STRING%2CASSISTANT_NAME%2CSUDO_USERS%2CREPLY_MESSAGE%2CSUPPORT_GROUP%2CUPDATES_CHANNEL&optionalEnvs=REPLY_MESSAGE%2CSUPPORT_GROUP%2CUPDATES_CHANNEL&API_IDDesc=User+Account+Telegram+API_ID+get+it+from+my.telegram.org%2Fapps&API_HASHDesc=User+Account+Telegram+API_HASH+get+it+from+my.telegram.org%2Fapps&BOT_TOKENDesc=Your+Telegram+Bot+Token%2C+get+it+from+%40Botfather+XD&SESSION_STRINGDesc=Pyrogram+Session+String+of+User+Account%2C+get+it+from+%40genStr_robot&ASSISTANT_NAMEDesc=Your+Video+Player%27s+assistant+username+without+%40&SUDO_USERSDesc=ID+of+Sudo+Users+who+can+use+Admin+commands+%28for+multiple+users+seperated+by+space%29&REPLY_MESSAGEDesc=A+reply+message+to+those+who+message+the+USER+account+in+PM.+Make+it+blank+if+you+do+not+need+this+feature.&SUPPORT_GROUPDesc=Support+Group+username+without+%40+%5BLeave+this+if+you+don%27t+have+one%5D&UPDATES_CHANNELDesc=Updates+Channel+username+without+%40+%5BLeave+this+if+you+don%27t+have+one%5D&SUPPORT_GROUPDefault=SafoTheBot&UPDATES_CHANNELDefault=AsmSafone&REPLY_MESSAGEDefault=Hello+Sir%2C+I%27m+a+bot+to+stream+videos+on+telegram+voice+chat%2C+not+having+time+to+chat+with+you+%F0%9F%98%82%21&referralCode=SAFONE"><img src="https://img.shields.io/badge/Deploy%20To%20Railway-blueviolet?style=for-the-badge&logo=railway" width="200""/></a></p>

### Heroku (Don't Complain)
<p><a href="https://heroku.com/deploy?template=https://github.com/AsmSafone/VideoPlayerBot"><img src="https://img.shields.io/badge/Deploy%20To%20Heroku-blueviolet?style=for-the-badge&logo=heroku" width="200""/></a></p>

## Commands (Set In Botfather)
```sh
start - Start The Bot
help - Show Help Message
play - Start Audio Streaming
stream - Start Video Streaming
pause - Pause The Current Stream
resume - Resume The Paused Stream
endstream - Stop Streaming & Left VC
```

## Config Vars
1. `API_ID` : User Account Telegram API_ID, get it from my.telegram.org
2. `API_HASH` : User Account Telegram API_HASH, get it from my.telegram.org
3. `BOT_TOKEN` : Your Telegram Bot Token, get it from @Botfather XD
4. `SESSION_STRING` : Pyrogram Session String of User Account, get it from [@genStr robot](http://t.me/genStr_robot) or [![genStr](https://img.shields.io/badge/repl.it-genStr-yellowgreen)](https://repl.it/@AsmSafone/genStr)
5. `ASSISTANT_NAME` : Your Video Player's assistant username without @.
6. `SUPPORT_GROUP` : Support Group username without @ [Leave this if you don't have one]
7. `UPDATES_CHANNEL` : Updates Channel username without @ [Leave this if you don't have one]
8. `SUDO_USERS` : ID of Users who can use Admins commands (for multiple users seperated by space)
9. `REPLY_MESSAGE` : A reply to those who message the USER account in PM. Leave it blank if you do not need this feature.

## Requirements
- Python 3.6 or Higher.
- Latest [FFmpeg Python](https://www.ffmpeg.org/).
- [Telegram API key](https://docs.pyrogram.org/intro/quickstart#enjoy-the-api).
- Pyrogram [String Session](http://t.me/genStr_robot) Of The Account.
- The User Account Needs To Be An Admin In The Group / Channel.

## Self Host
```sh
$ git clone -b main https://github.com/AsmSafone/VideoPlayerBot
$ cd VideoPlayerBot
$ sudo apt-get install python3-pip ffmpeg
$ pip3 install -U pip
$ pip3 install -U -r requirements.txt
# <create .env variables appropriately>
$ python3 main.py
```

## License
```sh
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
```

## Credits

- [Me](https://github.com/AsmSafone) for [Noting](https://github.com/AsmSafone/VideoPlayerBot) 😬
- [Dan](https://github.com/delivrance) for [Pyrogram](https://github.com/pyrogram/pyrogram) ❤️
- [MarshalX](https://github.com/MarshalX) for [pytgcalls](https://github.com/MarshalX/tgcalls) ❤️
- And Thanks To All [Contributors](https://github.com/AsmSafone/VideoPlayerBot/graphs/contributors)! ❤️
