import discord 

from db import database 
from discord.ext import commands

db = database.cursor()

"""
In case the bot was added to a server when it was offline, the prefix for it won't be there in the database.
So, when a message is sent, bot will check the database for the guild.
If it's not there, it'll add it with the default prefix
"""
class FixPrefix(commands.Cog):
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
        if not isinstance(msg.channel, discord.DMChannel):
            check = await self.check_prefix(str(msg.guild.id))
            if check is None:
                db.execute(f"INSERT INTO Prefix(guild, prefix) VALUES ('{msg.guild.id}','-')")
                print("Fixed prefix for a guild")
                database.commit()

        

def setup(client):
    client.add_cog(FixPrefix(client))
    print('FixPrefix')