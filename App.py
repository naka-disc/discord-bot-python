import os, datetime
import discord

# 監視先のVCチャンネルIDや、書き込み先チャンネルIDは環境変数から取得
# https://docs.python.org/ja/3/library/os.html#os.getenv
check_ch_id = os.getenv("DISCORD_VC_CHECK_TARGET_CH_ID")
post_ch_id  = os.getenv("DISCORD_VC_CHECK_POST_CH_ID")
bot_token   = os.getenv("DISCORD_VC_CHECK_BOT_TOKEN")


# 以下ディスコード用処理
client = discord.Client()
@client.event
async def on_voice_state_update(member, before, after):
    # 接続したmemberがbotの場合、記録は必要無い為無視。（byこはく
    if member.bot: return
    
    # print(member.name) # name
    # print(member.discriminator) # ID

    # member.guild.idは、該当メンバーが入退室したVCチャンネルID
    # これはintだけど、envから取ってる方がstrなので、strに合わせるためにstrに
    member_action_ch_id = str(member.guild.id)
    if member_action_ch_id == check_ch_id and (before.channel != after.channel):

        # 対象者の名前とID、現在時刻を取得
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
            await embedSender(
			        alert_channel,
			        EmbedGenerator(
				        '入室通知',
                        ":loud_sound: {channnelname} ボイスチャンネル".format(channnelname = after.channel.name),
				        name,
				    )
			    )
            
#            msg = "入室通知: {now} | {name}".format(now = now, name = name)
#            await alert_channel.send(msg)
        elif after.channel is None: 
            await embedSender(
			        alert_channel,
			        EmbedGenerator(
				        '退室通知',
                        ":loud_sound: {channnelname} ボイスチャンネル".format(channnelname = before.channel.name),
				        name,
				    )
			    )
#            msg = "退室通知: {now} | {name}".format(now = now, name = name)
#            await alert_channel.send(msg)


# 書式変更済みタイムスタンプを返す（byこはく
def TimeStamp(): return datetime.datetime.now().strftime('%Y年%m月%d日　%H時%M分')

# Embedオブジェクト出力（byこはく
async def embedSender(channel, embed): await channel.send(embed = embed)

# Embedオブジェクト作成（byこはく
def EmbedGenerator(title, logLocation, memberName = ''):

	embedMessages = ''

	# タイムスタンプ出力
	embedMessages += 'TimeStamp：'
	embedMessages += TimeStamp()
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
	return discord.Embed(title = title, description = embedMessages)# Embed生成


client.run(bot_token)
