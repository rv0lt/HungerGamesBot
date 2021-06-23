import asyncio
from asyncio.tasks import sleep
import os
import discord
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('TOKEN')
client = discord.Client()

countdown_started = False
game_started = False



@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    global countdown_started
    global game_started
    msg = message.content
        
    
    if msg.startswith('hg!ping'):
        await message.channel.send('Hello!')

    elif msg.startswith('hg!start'):
        if countdown_started:
            await message.channel.send("Game already started")
            return

        countdown_started = True
        await message.channel.send("Game Started, 1 minute to join")
        await asyncio.sleep(20)
        await message.channel.send("40 seconds left to join")
        await asyncio.sleep(20)
        await message.channel.send("20 seconds left to join")
        await asyncio.sleep(20)
        await message.channel.send("10 seconds left to join")
        await asyncio.sleep(5)
        await message.channel.send("5 seconds left to join")
        await asyncio.sleep(5)
        await message.channel.send("Starting game")
        game_started = True

    elif msg.startswith('hg!join'):
        if not countdown_started:
            await message.channel.send("There is no game active")
        elif game_started:
            await message.channel.send("Game already started, you cannot join now")
        else:
            await message.channel.send(str(message.author) + " has joined the game")



client.run(token)
