
import os
import random
import discord
import interactions
from dotenv import load_dotenv

load_dotenv()
token = ""

client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    print("Logged in as a bot {0.user}".format(client))
    channel = client.get_channel(1311071586530623508) 
    await channel.send("I have awakened")

@client.event
async def on_message(message):
    channel = client.get_channel(1311071586530623508) 
    if message.author == client.user:
        return
    elif message.author.id == 265614755220160512:
        await channel.send("you stink of the foulest stench i have ever smelt, return from whence you came")
    else:
        await channel.send("I hear whispers in the night")
    
    
client.run(token)