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

    async def check_prefix(self, guild):
        db.execute(f"SELECT prefix FROM Prefix WHERE guild = '{guild}'")
        for row in db:
            final = str(row).strip("('',)") #It's a tuple in the database, with a comma after the prefix string.
            return final

    @commands.Cog.listener()
    async def on_message(self, msg):
        check = await self.check_prefix(str(msg.guild.id))
        if check is None:
            db.execute(f"INSERT INTO Prefix(guild, prefix) VALUES ('{msg.guild.id}','-')")
            print("Fixed prefix for a guild")
            database.commit()

        

def setup(client):
    client.add_cog(FixPrefix(client))
    print('FixPrefix')