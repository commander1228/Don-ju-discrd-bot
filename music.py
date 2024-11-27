
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
    async def play(ctx,self,url):
            server = self.message.guild
            voice_channel = server.voice_client

            async with self.typing():
                filename = await YTDLSource.from_url(url, loop=self.bot.loop)
                voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
            await self.send('**Now playing:** {}'.format(filename))


    @commands.command(name='pause', help='This command pauses the song')
    async def pause(ctx,self):
        voice_client = self.message.guild.voice_client
        if voice_client.is_playing():
            await voice_client.pause()
        else:
            await self.send("The bot is not playing anything at the moment.")
        
    @commands.command(name='resume', help='Resumes the song')
    async def resume(ctx,self):
        voice_client = self.message.guild.voice_client
        if voice_client.is_paused():
            await voice_client.resume()
        else:
            await self.send("The commands was not playing anything before this. Use play_song command")

    @commands.command(name='stop', help='Stops the song')
    async def stop(ctx,self):
        voice_client = self.message.guild.voice_client
        if voice_client.is_playing():
            await voice_client.stop()
        else:
            await self.send("The bot is not playing anything at the moment.")
            
        