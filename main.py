
import os
import random
import discord
from dotenv import load_dotenv

load_dotenv()
token = ""

client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    print("Logged in as a bot {0.user}".format(client))

client.run(token)