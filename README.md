# Telegram Video Player Bot (Py-TgCalls)
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

An Telegram Bot By [@AsmSafone](https://t.me/AsmSafone) To Stream Videos In Telegram Voice Chat Of Both Groups & Channels. Supports Live Streams, YouTube Videos & Telegram Media !!

## Special Features

- Playlist, queue, 24x7 live stream
- Supports Live streaming from youtube
- Starts live stream if no songs in playlist
- Automatic playback even if heroku restarts
- Show current playing position of the audio
- Change Voice chat title to current playing song name
- Automatically downloads audio for the first two tracks in the playlist to ensure smooth playing

## Deploy Own Bot

### Heroku (The Easiest Way)
<p><a href="https://heroku.com/deploy?template=https://github.com/AsmSafone/VideoPlayerBot/tree/alpha"><img src="https://img.shields.io/badge/Deploy%20To%20Heroku-blueviolet?style=for-the-badge&logo=heroku" width="200""/></a></p>

### Railway (At Your Own Risk)
<p><a href="https://railway.app/new/template?template=https%3A%2F%2Fgithub.com%2FAsmSafone%2FVideoPlayerBot%2Ftree%2Falpha&envs=API_ID%2CAPI_HASH%2CBOT_TOKEN%2CSESSION_STRING%2CCHAT_ID%2CLOG_GROUP%2CAUTH_USERS%2CADMIN_ONLY%2CSTARTUP_STREAM%2CREPLY_MESSAGE&optionalEnvs=LOG_GROUP%2CADMIN_ONLY%2CREPLY_MESSAGE&API_IDDesc=Your+Telegram+API_ID+get+it+from+my.telegram.org%2Fapps&API_HASHDesc=Your+Telegram+API_HASH+get+it+from+my.telegram.org%2Fapps&BOT_TOKENDesc=Bot+token+of+your+bot%2C+get+from+%40Botfather&SESSION_STRINGDesc=Session+string%2C+use+%40genStr_robot+to+generate+pyrogram+session+string&CHAT_IDDesc=ID+of+Channel+or+Group+where+the+Bot+plays+Live%2FMusic%2FYouTube+Lives&LOG_GROUPDesc=ID+of+the+group+to+send+playlist+if+CHAT+is+a+Group%2C+if+channel+then+leave+blank&AUTH_USERSDesc=ID+of+Users+who+can+use+Admin+commands+%28for+multiple+users+seperated+by+space%29&ADMIN_ONLYDesc=Change+it+to+%27True%27+If+you+want+to+make+%2Fplay+commands+only+for+admins+of+CHAT.+By+default+%2Fplay+is+available+for+all&STARTUP_STREAMDesc=URL+of+Live+Stream+or+Youtube+Live+video+link+to+stream+with+bootup&REPLY_MESSAGEDesc=A+reply+message+to+those+who+message+the+USER+account+in+PM.+Make+it+blank+if+you+do+not+need+this+feature.&ADMIN_ONLYDefault=False&STREAM_URLDefault=https://youtu.be/36YnV9STBqc&REPLY_MESSAGEDefault=Hello Sir, I'm a bot to stream videos on telegram voice chat, not having time to chat with you 😂!"> <img src="https://img.shields.io/badge/Deploy%20To%20Railway-blueviolet?style=for-the-badge&logo=railway" width="200""/></a></p>


## Config Vars
1. `API_ID` : User Account Telegram API_ID, get it from https://my.telegram.org
2. `API_HASH` : User Account Telegram API_HASH, get it from https://my.telegram.org
3. `BOT_TOKEN` : Your Telegram Bot Token, get it from [@Botfather](https://t.me/botfather) XD
4. `SESSION_STRING` : Pyrogram Session String of User Account, get it from [@genStr robot](http://t.me/genStr_robot) or [![genStr](https://img.shields.io/badge/repl.it-genStr-yellowgreen)](https://repl.it/@AsmSafone/genStr)
5. `CHAT_ID` : ID of Channel or Group where the bot will stream videos.
6. `LOG_GROUP` : Group to send Playlist, if CHAT_ID is a Group.
7. `AUTH_USERS` : ID of Users who can use Admins commands (for multiple users seperated by space).
8. `REPLY_MESSAGE` : A reply to those who message the USER account in PM. Leave it blank if you do not need this feature.
9. `ADMIN_ONLY` : Pass 'True' If you want to make /play commands only for admins. By default /play is available for all.
10. `STARTUP_STREAM` : Stream URL of live station or a youtube live video to stream when the bot starts.
11. `HEROKU_API_KEY`: Your Heroku api key. Get it from [here](https://dashboard.heroku.com/account)
12. `HEROKU_APP_NAME`: Name of your Heroku app if deploying to heroku.
13. `IS_NONSTOP_STREAM`: Change it to 'False' If you want to disable nonstop 24x7 live stream feature. By default it is enabled.

## Requirements
- Python 3.6 or Higher.
- Latest [FFmpeg](https://www.ffmpeg.org/).
- [Telegram API Key](https://docs.pyrogram.org/intro/quickstart#enjoy-the-api).
- Pyrogram [String Session](http://t.me/genStr_robot) Of The Account.
- The User Account Needs To Be An Admin In The Group / Channel.

## Self Host
```sh
$ git clone -b alpha https://github.com/AsmSafone/VideoPlayerBot
$ cd VideoPlayerBot
$ sudo apt install git curl python3-pip ffmpeg -y
$ pip3 install -U pip
$ curl -sL https://deb.nodesource.com/setup_16.x | sudo -E bash -
$ sudo apt install -y nodejs
$ sudo apt install build-essential
$ sudo npm install pm2@latest -g
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
- [Laky-64](https://github.com/Laky-64) for [Py-TgCalls](https://github.com/pytgcalls/pytgcalls) ❤️
- And Thanks To All [Contributors](https://github.com/AsmSafone/VideoPlayerBot/graphs/contributors)! ❤️
