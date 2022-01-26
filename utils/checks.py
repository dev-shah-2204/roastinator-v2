import discord
import json 
import requests
import os

from dotenv import load_dotenv
from db import *


load_dotenv()


def get_automod_status(guild: str):
    """
    Get the automod status for a guild
    """
    with open('./cache/automod.json', 'r') as f:
        cache = json.load(f)
    
    if guild not in cache:
        db.execute(f"SELECT _status FROM AutoMod WHERE guild = '{guild}'")
        status = db.fetchone()
        
        if status is None:
            db.execute(f"INSERT INTO AutoMod(guild, _status) VALUES ('{guild}', 'disabled')")
            db.execute(f"CREATE TABLE IF NOT EXISTS am_{guild}(words VARCHAR(40) PRIMARY KEY)")
            database.commit()
            status = 'disabled'
            
        cache[guild] = {}
        cache[guild]['status'] = status
        cache[guild]['blacklist'] = [] 

        with open("./cache/automod.json", "w") as f:
            json.dump(cache, f)
            
    else:
        status = cache[guild]['status']
            
        return status 
        

def get_blacklist(guild):
    """
    Get the blacklist for a guild
    """
    status = get_automod_status(guild)
    
    with open('./cache/automod.json', 'r') as f:
        cache = json.load(f)
            
    if guild not in cache:
        db.execute(f"SELECT * FROM am_{guild}")
        blacklist = db.fetchall()
        
        for word in blacklist:
            cache[guild]['blacklist'].append(word[0])
        
        with open("./cache/automod.json", "w") as f:
            json.dump(cache, f)
              
    else:
        blacklist = cache[guild]['blacklist']

    return blacklist


def get_server_prefix(msg):
    if isinstance(msg.channel, discord.DMChannel):
        return '-'

    with open('./cache/prefix.json', 'r') as f:
        cache = json.load(f)

    if str(msg.guild.id) in cache:
        return cache[str(msg.guild.id)]


    db.execute(f"SELECT prefix FROM Prefix WHERE guild = '{msg.guild.id}'")
    prefix = db.fetchone()

    if prefix is None:
        db.execute(f"INSERT INTO Prefix(guild, prefix) VALUES ('{msg.guild.id}', '-')")
        database.commit()
        prefix = '-'
    else:
        prefix = prefix[0]

    cache[str(msg.guild.id)] = prefix

    with open('./cache/prefix.json', 'w') as f:
        json.dump(cache, f)

    return prefix


def get_command_blacklist():
    """
    Get the command list of people that are not allowed to use the bot
    """
    with open('./cache/banned.json', 'r') as f:
        cache = json.load(f)

    if 'banned' in cache:
        return cache['banned']

    else:
        db.execute(f"SELECT * from command_blacklist")
        blacklist = db.fetchall()
        banned_people = []

        for tup in blacklist:
            banned_people.append(str(tup[0]))

        cache["banned"] = banned_people

        with open('./cache/banned.json', 'w') as f:
            json.dump(cache, f)

        return banned_people

def bool_str(variable):
    """
    Convert boolean values to string: Yes/No
    """
    if variable == True:
        return 'Yes'
    if variable == False:
        return 'No'


def get_steam_id_from_url(url):
    """
    Gets the steam ID of a person from their steam profile URL
    """
    url = url.replace('https://', '')
    url = url.replace('steamcommunity.com/profiles/', '')
    url = url.replace('steamcommunity.com/id/', '')
    url = url.strip('/')

    try:
        id = int(url)  # If they're not using a vanity url
        return id
    except ValueError:
        id = requests.get(f"http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={os.getenv('STEAM_API_KEY')}&vanityurl={url}").json()  # To get ID from vanity URL

        try:
            return id['response']['steamid']
        except KeyError:
            return None
