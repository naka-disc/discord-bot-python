# discord-bot-vc-check
Discordのボイスチャットチャンネルの入退室を監視するBot


## 前提
 - SQLite3が使えること
 - Python3が使えること


## 準備
```sh
python -m venv .venv
source .venv/bin/activate
```

```sh
pip install discord
```

```sh
export DISCORD_VC_CHECK_TARGET_CH_ID=000000000000000000
export DISCORD_VC_CHECK_POST_CH_ID=000000000000000000
export DISCORD_VC_CHECK_BOT_TOKEN="xxxxxxxxx"
python App.py
```
