import discord
import youtube_dl
import os

#VOCÊ PRECISA DO YOUTUBE-DL INSTALADO, PARA ISSO DIGITE "pip install youtube_dl" NO CMD!
client = discord.Client()

players = {}
COR = 0xF7FE2E

@client.event
async def on_ready():
    print(client.user.name)
    print("===================")

@client.event
async def on_message(message):
    if message.content.startswith('!entrar'):
        try:
            channel = message.author.voice.voice_channel
            await client.send_message(message.channel, "Entrei no canal: `{}`.".format(channel))
            await client.join_voice_channel(channel)
        except discord.errors.InvalidArgument:
            await client.send_message(message.channel, "{}, já estou em um canal de voz!".format(message.author.mention))
        except Exception as error:
            await client.send_message(message.channel, "Ein Error: ```{error}```".format(error=error))

    if message.content.startswith('!sair'):
        try:
            mscleave = discord.Embed(
                title="\n",
                color=COR,
                description="Não estou mais no canal!"
            )
            voice_client = client.voice_client_in(message.server)
            await client.send_message(message.channel, embed=mscleave)
            await voice_client.disconnect()
        except AttributeError:
            embed = discord.Embed(
                title='ERRO',
                color=COR,
                description='Não estou em nenhum canal de voz!'
            )
            await client.send_message(message.channel, embed=embed)
        except Exception as Hugo:
            await client.send_message(message.channel, "Ein Error: ```{haus}```".format(haus=Hugo))

    if message.content.startswith('!play'):
        try:
            yt_url = message.content[6:]
            if client.is_voice_connected(message.server):
                try:
                    voice = client.voice_client_in(message.server)
                    players[message.server.id].stop()
                    player = await voice.create_ytdl_player('ytsearch: {}'.format(yt_url))
                    players[message.server.id] = player
                    player.start()
                    mscemb = discord.Embed(
                        title="🎼 Informações da música:",
                        color=COR
                    )
                    mscemb.add_field(name="📌 Título:", value="`{}`".format(player.title))
                    mscemb.add_field(name="🔎 Visualizações:", value="`{}`".format(player.views))
                    mscemb.add_field(name="🔔 Enviado em:", value="`{}`".format(player.uploaded_date))
                    mscemb.add_field(name="👤 Enviado por:", value="`{}`".format(player.uploadeder))
                    mscemb.add_field(name="🕓 Duração:", value="`{}`".format(player.uploadeder))
                    mscemb.set_thumbnail(url="{}.png".format(player.thumbnail))
                    mscemb.add_field(name="👍 Likes:", value="`{}`".format(player.likes))
                    mscemb.add_field(name="👎 Deslikes:", value="`{}`".format(player.dislikes))
                    await client.send_message(message.channel, embed=mscemb)
                except Exception as e:
                    await client.send_message(message.server, "Error: [{error}]".format(error=e))

            if not client.is_voice_connected(message.server):
                try:
                    channel = message.author.voice.voice_channel
                    voice = await client.join_voice_channel(channel)
                    player = await voice.create_ytdl_player('ytsearch: {}'.format(yt_url))
                    players[message.server.id] = player
                    player.start()
                    mscemb2 = discord.Embed(
                        title="🎼 Informações da música:",
                        color=COR
                    )
                    mscemb2.add_field(name="📌 Título:", value="`{}`".format(player.title))
                    mscemb2.add_field(name="🔎 Visualizações:", value="`{}`".format(player.views))
                    mscemb2.add_field(name="🔔 Enviado em:", value="`{}`".format(player.uploaded_date))
                    mscemb2.add_field(name="👤 Enviado por:", value="`{}`".format(player.uploadeder))
                    mscemb2.add_field(name="🕓 Duração:", value="`{}`".format(player.uploadeder))
                    mscemb2.add_field(name="👍 Likes:", value="`{}`".format(player.likes))
                    mscemb2.add_field(name="👎 Deslikes:", value="`{}`".format(player.dislikes))
                    await client.send_message(message.channel, embed=mscemb2)
                except Exception as error:
                    await client.send_message(message.channel, "Error: [{error}]".format(error=error))
        except Exception as e:
            await client.send_message(message.channel, "Error: [{error}]".format(error=e))




    if message.content.startswith('!pause'):
        try:
            mscpause = discord.Embed(
                title="\n",
                color=COR,
                description="Música pausada com sucesso!"
            )
            await client.send_message(message.channel, embed=mscpause)
            players[message.server.id].pause()
        except Exception as error:
            await client.send_message(message.channel, "Error: [{error}]".format(error=error))
    if message.content.startswith('!resume'):
        try:
            mscresume = discord.Embed(
                title="\n",
                color=COR,
                description="Musica despausada com sucesso!"
            )
            await client.send_message(message.channel, embed=mscresume)
            players[message.server.id].resume()
        except Exception as error:
            await client.send_message(message.channel, "Error: [{error}]".format(error=error))


client.run(os.environ.get("BOT_TOKEN"))
