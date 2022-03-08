# discord-bot-python
- DiscordのBot。
- Python3で作成。


## 前提
 - SQLite3が使えること
 - Python3が使えること


## 準備
```sh
python -m venv .venv
source .venv/bin/activate
```

```sh
pip install -r requirements.txt
```

```sh
# 内部で使うため環境変数をセット
# チェック対象VCのID、メッセージ書き込み先CHのID、Botのトークン
export DISCORD_VC_CHECK_TARGET_CH_ID=000000000000000000
export DISCORD_VC_CHECK_POST_CH_ID=000000000000000000
export DISCORD_VC_CHECK_BOT_TOKEN="xxxxxxxxx"
```

```sh
# ローカルで簡単に動かすとき
python App.py

# サーバーで、簡単に動かしっぱなしにしたいとき
nohup python App.py > /dev/null 2>&1 &
# 消すときはプロセスID特定してKill
ps aux | grep python
kill xxxx
```
