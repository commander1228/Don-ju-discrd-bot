
import asyncio
import os
import random
import discord
import yt_dlp as youtube_dl
from discord.ext import commands,tasks
from dotenv import load_dotenv
import music
import ffmpeg

load_dotenv()
token = ""
intents = discord.Intents().all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!',intents=intents)

@bot.event
async def on_ready():
    await bot.add_cog(music.music(bot))

bot.run(token)