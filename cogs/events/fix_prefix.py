import discord 
import json

from db import * 
from discord.ext import commands


class FixPrefix(commands.Cog):
    """
    In case the bot was added to a server when it was offline, the prefix for it won't be there in the database.
    So, when a message is sent, bot will check the database for the guild.
    If it's not there, it'll add it with the default prefix
    """
    def __init__(self, client):
        self.client = client
    
    server_list = []

    async def check_prefix(self, guild):
        if guild not in self.server_list: #We don't want to call the database everytime
            db.execute(f"SELECT prefix FROM Prefix WHERE guild = '{guild}'")
            for row in db:
                final = str(row).strip("('',)") #It's a tuple in the database, with a comma after the prefix string.
                return final
                self.server_list.append(guild)
        if guild in self.server_list:
            return True #If we don't return something, the bot will think that the server doesn't have a prefix and add it into the database.

    @commands.Cog.listener()
    async def on_message(self, msg):
        if not msg.author.bot and not isinstance(msg.channel, discord.DMChannel):
            check = await self.check_prefix(str(msg.guild.id))
            if check is None:
                db.execute(f"INSERT INTO Prefix(guild, prefix) VALUES ('{msg.guild.id}','-')")
                print("Fixed prefix for a guild")
                database.commit()

                with open('prefix.json', 'r') as f:
                    cache = json.load(f)

                cache[str(msg.guild.id)] = '-'

                with open('prefix.json', 'w') as g:
                    json.dump(cache, g)

        

def setup(client):
    client.add_cog(FixPrefix(client))
    print('FixPrefix')