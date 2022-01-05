import json 
import discord 

from discord.ext import commands 
from db import *

def get_prefix(bot, message):
    with open('./cache/prefix.json', 'r') as f:
        cache = json.load(f)
    
    guild = str(message.guild.id)
    if guild in cache:
        return commands.when_mentioned_or(cache[guild])(bot, message)
    
    else:
        db.execute(f"SELECT prefix FROM Prefix WHERE guild = {guild}")
        prefix = db.fetchone()

        if prefix is None:
            db.execute(f"INSERT INTO Prefix(guild, prefix) VALUES ('{guild}', '-')")  # Default prefix is - 
            database.commit()
            cache[guild] = '-'
        else:
            cache[guild] = prefix[0]
        
        with open('./cache/prefix.json', 'w') as f:
            json.dump(cache, f)
            
        return commands.when_mentioned_or(prefix[0])(bot, message)


class Roastinator(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(
            command_prefix = get_prefix,
            intents=discord.Intents.all(),
            case_insensitive=True,
            allowed_mentions=discord.AllowedMentions(everyone=False),  # Set this according to your own preference
            owner_id=os.getenv('discord_id')  # Enter your discord ID here
        )


if __name__ == "__main__":
    raise RuntimeError("Make sure you're running the main.py file and not the bot.py file")
    exit()
