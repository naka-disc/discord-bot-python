import os, datetime, sqlite3
import discord

# 監視先のVCチャンネルIDや、書き込み先チャンネルIDは環境変数から取得
# https://docs.python.org/ja/3/library/os.html#os.getenv
check_ch_id = os.getenv("DISCORD_VC_CHECK_TARGET_CH_ID")
post_ch_id  = os.getenv("DISCORD_VC_CHECK_POST_CH_ID")
bot_token   = os.getenv("DISCORD_VC_CHECK_BOT_TOKEN")

# 永続化用のDB設定 今回は簡易的に済ませるため、SQLite3を採用
DB_FILE_PATH = "main.sqlite3"
connection = sqlite3.connect(DB_FILE_PATH)
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
connection.row_factory = dict_factory
cursor = connection.cursor()

# 以下ディスコード用処理
client = discord.Client()
@client.event
async def on_voice_state_update(member, before, after):
    # 接続したmemberがbotの場合、記録は必要無い為無視。（byこはく
    if member.bot: return
    print()
    
    # print(member.name) # name
    # print(member.discriminator) # ID

    # member.guild.idは、該当メンバーが入退室したVCチャンネルID
    # これはintだけど、envから取ってる方がstrなので、strに合わせるためにstrに
    member_action_ch_id = str(member.guild.id)
    if member_action_ch_id == check_ch_id and (before.channel != after.channel):

        # 対象者の名前とID、タグ、現在時刻を取得
        id = member.id
        name = member.name
        discriminator = member.discriminator
        now = datetime.datetime.now()

        # 書き込み先のチャンネルを取得
        # envから取得したpost_ch_idはstr形式なので、
        # intで数値に変えないとライブラリ内部でのマッチ処理で合わない
        alert_channel = client.get_channel(int(post_ch_id))

        #以下、入退室ログはEmbedオブジェクトによる通知に致しました。(byこはく
        # 入室か退室かで処理分岐
        # 書き込み先のチャンネルに定型文を書き出し
        if before.channel is None:
            # 入室ログをINSERT
            add_vc_access_records(id, name, discriminator, now)

            await sendEmbed(
                    alert_channel,
                    createEmbed(
                        '入室通知',
                        ":loud_sound: {channnelname} ボイスチャンネル".format(channnelname = after.channel.name),
                        name,
                    )
                )
            
        elif after.channel is None:
            # 直近の入室ログを取得
            # data = get_recent_vc_access_records(discriminator)
            # print(data)

            # VCの入退室ログに退室日時を登録
            # 滞在時間秒数は、分と秒に換算したいので、ここで処理
            total_second = edit_vc_access_records(id, now)
            minutes = int(total_second / 60)
            second = int(total_second % 60)

            await sendEmbed(
                    alert_channel,
                    createEmbed(
                        '退室通知',
                        ":loud_sound: {channnelname} ボイスチャンネル".format(channnelname = after.channel.name),
                        name,
                    )
                )

# 指定メンバーの、直近の入退室ログを取得
def get_recent_vc_access_records(member_id: str) -> dict:
    # 指定メンバーの、直近の入退室ログを取得
    sql = "SELECT * FROM vc_access_records WHERE member_id = ? ORDER BY in_datetime DESC"
    cursor.execute(sql, (member_id,))
    record = cursor.fetchall()[0]
    return record

# 入退室ログを登録（＝入室時の処理）
def add_vc_access_records(member_id: str, member_name: str, member_discriminator: str, target_date: datetime.datetime) -> None:
    # メンバー情報と、入室情報だけの入退室ログを登録
    sql = "INSERT INTO vc_access_records (member_id, member_name, member_discriminator, in_datetime) VALUES (?, ?, ?, ?);"
    data = (member_id, member_name, member_discriminator, target_date.strftime('%Y/%m/%d %H:%M:%S'))
    cursor.execute(sql, data)
    connection.commit()

# 入退室ログを更新（＝退室時の処理）
def edit_vc_access_records(member_id: str, target_date: datetime.datetime) -> float:
    # 該当メンバーの、直近の入退室ログを取得
    # 入室時に、入室時間しか持たせてないデータをINSERTしているので、直近のをとってくれば問題ないはず
    e = get_recent_vc_access_records(member_id)
    
    # 滞在時間の秒数を算出
    in_datetime = datetime.datetime.strptime(e["in_datetime"], "%Y/%m/%d %H:%M:%S")
    d = target_date - in_datetime
    total_second = d.total_seconds()

    # 取得した入退室ログに、退出情報と滞在時価を付与
    data = (target_date.strftime('%Y/%m/%d %H:%M:%S'), total_second, e["id"])
    sql = "UPDATE vc_access_records SET out_datetime = ?, stay_second = ? WHERE id = ?"
    cursor.execute(sql, data)
    connection.commit()

    # 出力用に、滞在時間秒数を返す
    return total_second

# Embedオブジェクト出力（byこはく
async def sendEmbed(channel: any, embed: discord.Embed) -> any:
    await channel.send(embed = embed)

# Embedオブジェクト作成（byこはく
def createEmbed(title, logLocation, memberName = '') -> discord.Embed:

    embedMessages = ''

    # タイムスタンプ出力
    embedMessages += 'TimeStamp：'
    embedMessages += datetime.datetime.now().strftime('%Y年%m月%d日　%H時%M分')
    embedMessages += '\n'

    # メンバー名出力
    embedMessages += 'Member：'
    embedMessages += memberName
    embedMessages += '\n'

    # 記録場所
    embedMessages += 'LogLocation：'
    embedMessages += logLocation
    embedMessages += '\n'

    # Embed作成
    return discord.Embed(title = title, description = embedMessages)


client.run(bot_token)
