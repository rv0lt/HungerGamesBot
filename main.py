import asyncio
import os
import discord
import sqlite3
import random
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('TOKEN')
client = discord.Client()
database = "database.db"

countdown_started = False
game_started = False
alliances = {}
alliances_to_accept = {}

districts = [
    'D1 Male',
    'D1 Female',
    'D2 Male',
    'D2 Female',
    'D3 Male',
    'D3 Female',
    'D4 Male',
    'D4 Female',
    'D5 Male',
    'D5 Female',
    'D6 Male',
    'D6 Female',
    'D7 Male',
    'D7 Female',
    'D8 Male',
    'D8 Female',  
    'D9 Male',
    'D9 Female',  
    'D10 Male',
    'D10 Female',
    'D11 Male',
    'D11 Female', 
    'D12 Male',
    'D12 Female',   
]
districts_left = []

#initiate datbase to begin the play
def initiate_database():
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute('''
        DROP TABLE IF EXISTS players
            ''')
    cur.execute('''
        CREATE TABLE players (
            player_name text, 
            score int, 
            district text,
            ally text,
            PRIMARY KEY (player_name)
            )
        ''') 
    con.commit()
    con.close()

#insert a new player into the database
def insert_player(player, district_left):
    con = sqlite3.connect(database)
    cur = con.cursor()

    score = int(random.uniform(1,12))
    district = random.choice(district_left)
    district_left = [x for x in district_left if x != district]

    cur.execute('''
        INSERT INTO players VALUES (?,?,?,?)
        ''', (player, score, district,""))
    con.commit()
    con.close() 

    return district_left

#check if a player is in the DB
def check_player(player_name):
    con = sqlite3.connect(database)
    cur = con.cursor()
    
    cur.execute('''
        SELECT * FROM players WHERE player_name=?
    ''', (player_name,))
    res = cur.fetchone()

    return res != None

#function to write the number of players, theirs scores and districts assigned
def how_many():
    con = sqlite3.connect(database)
    cur = con.cursor()

    message = " -------------------- \n Player_name , score, district \n -------------------- \n"
    for row in cur.execute('SELECT * FROM players'):
        message += str(row)
        message += "\n -------------------- \n"
    print(message)
    return message

#check alliances madem and write the alliances
def check_alliances():
    message = " -------------------- \n Alliances maden: \n"
    for ally_1 in alliances:
        if alliances[ally_1] == "":
            continue
        if alliances[ally_1][1]:
            ally_2 = alliances[ally_1][0]
            if alliances[ally_2] == "":
                continue
            if alliances[ally_2][1]:
                message+="{} allied {}".format(ally_1,ally_2)
                message+="\n--------------------n"
    print(message)
    return message

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    global countdown_started
    global game_started
    global districts_left
    global alliances
    global alliances_to_accept
    msg = message.content
    
    if msg.startswith('hg!ping'):
        await message.channel.send('Hello!')

    elif msg.startswith('hg!start'):
        if countdown_started:
            await message.channel.send("Game already started")
            return

        districts_left = districts
        countdown_started = True
        initiate_database()
        ####countdown to join the match
        await message.channel.send("Game Started, 1 minute to join\n Write hg!join to join")
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
        #await message.channel.send(how_many())
        #######Countdown to submit alliances
        await message.channel.send("You have 2 minutes to talk and submit alliances\n Type hg!alliance and the player_name you want to ally with\n The other players need to write hg!confirm in order to be a valid alliance \n Right now you can only ally one player")
        await asyncio.sleep(60)
        await message.channel.send("1 minute left to ally")
        await asyncio.sleep(30)
        await message.channel.send("30 seconds left to ally")
        await asyncio.sleep(15)
        await message.channel.send("15 seconds left to ally")
        await asyncio.sleep(10)
        await message.channel.send("5 seconds left to ally")    
    
        print(alliances)
        await message.channel.send(check_alliances())
        #########




    elif msg.startswith('hg!join'):
        if not countdown_started:
            await message.channel.send("There is no game active")
        elif game_started:
            await message.channel.send("Game already started, you cannot join now")
        else:

            player = str(message.author)
            districts_left = insert_player(player, districts_left)
            alliances[player] = ""
            await message.channel.send(player + " has joined the game")
            print(districts_left)
    elif msg.startswith('hg!alliance'):
        ally = msg.split('hg!alliance ',1)[1]
        author = str(message.author)
        #check if the proposed ally exists
        exist = check_player(ally)
        if exist:
            await message.channel.send(ally + " write hg!confirm to confirm alliance with " + str(message.author))
            alliances[author] = (ally,False)
            alliances[ally] = (author,False)
            alliances_to_accept[ally] = author
            print(alliances)
            print(alliances_to_accept)
        else:
            await message.channel.send(ally + "is not a player of this game")
    elif msg.startswith('hg!confirm'):
        author = str(message.author)
        #check if user has a alliance to accept
        ally = alliances_to_accept.get(author)[1]
        if ally == None:
            await message.channel.send(author + " has no alliance to confirm")
        else:
            alliances[author] = (ally, True)
            alliances[ally] = (author, True)
            alliances_to_accept.pop(author)
            await message.channel.send ("{} and {} are now allies".format(author,ally))
            print(alliances)
            print(alliances_to_accept)
client.run(token)
