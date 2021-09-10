echo "[INFO] - FETCHING UPSTREAM REPO ..."
git clone https://github.com/AsmSafone/VideoPlayerBot.git /VideoPlayerBot
cd /VideoPlayerBot
echo "[INFO] - INSTALLING REQUIREMENTS ..."
pip3 install -U -r requirements.txt
echo "[INFO] - STARTING VIDEO PLAYER BOT ..."
python3 -m bot
