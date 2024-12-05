
import asyncio
import os
import random
import discord
import yt_dlp as youtube_dl
from discord.ext import commands,tasks
from dotenv import load_dotenv
import ffmpeg

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename

class music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.songQue = []

    async def playSong(self,url,ctx: commands.Context):

        await ctx.send('**Now playing:** {}'.format(url))
        server = ctx.message.guild
        voiceChannel = server.voice_client
        filename = await YTDLSource.from_url(url,loop = self.bot.loop)
        print(self.songQue)
        def afterPlaying(_):
            self.bot.loop.create_task(self.playNextSong(ctx))
        voiceChannel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename),after=afterPlaying)

    async def playNextSong(self,ctx:commands.Context):
        print(self.songQue)
        if len(self.songQue) == 0:
            pass
        else:
            songUrl = self.songQue[0]
            self.songQue = self.songQue[1:]
            await self.playSong(songUrl,ctx)



    @commands.command(name='join', help='Tells the bot to join the voice channel')
    async def join(ctx,self):
        if not self.message.author.voice:
            await self.send("{} is not connected to a voice channel".format(self.message.author.name))
            return
        else:
            channel = self.message.author.voice.channel
        await channel.connect()

    @commands.command(name='leave', help='To make the bot leave the voice channel')
    async def leave(ctx,self):
        voice_client = self.message.guild.voice_client
        if voice_client.is_connected():
            await voice_client.disconnect()
        else:
            await self.send("The bot is not connected to a voice channel.")
        

    @commands.command(name='play', help='To play song')
    async def play(self,ctx,url):
            if ctx.voice_client.is_playing():
                self.songQue.append(url)
                await ctx.send(f"Added to queue: {url}")
                print (self.songQue)
                return
            else:
                async with ctx.typing():
                    await self.playSong(url,ctx)


    @commands.command(name='pause', help='This command pauses the song')
    async def pause(ctx,self):
        voice_client = self.message.guild.voice_client
        if voice_client.is_playing():
             voice_client.pause()
        else:
            await self.send("The bot is not playing anything at the moment.")
        
    @commands.command(name='resume', help='Resumes the song')
    async def resume(ctx,self):
        voice_client = self.message.guild.voice_client
        if voice_client.is_paused():
             voice_client.resume()
        else:
            await self.send("The commands was not playing anything before this. Use play_song command")

    @commands.command(name='stop', help='Stops the song')
    async def stop(ctx,self):
        voice_client = self.message.guild.voice_client
        if voice_client.is_playing():
             voice_client.stop()
        else:
            await self.send("The bot is not playing anything at the moment.")

    @commands.command(name='skip',help="skips the song aidens playing")
    async def skip(self,ctx):
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            self.playNextSong
            return
        else:
            await ctx.send("no song is currently playing")
            return
