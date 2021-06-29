import discord
import mysql.connector

from discord.ext import commands
from db import database

db = database.cursor(buffered = True)

class OnGuildJoin(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        """
        When the bot joins a server, we want to assign the default prefix for that server.
        """
        try:
            db.execute("INSERT INTO Prefix ('guild', 'prefix') VALUES (%s, %s)",(guild.id, '-')) #My table is called Prefix
        except:
            db.execute(f"UPDATE Prefix SET prefix = '-' WHERE guild = '{guild.id}'")#Reset prefix if bot is re-added
        database.commit()


def setup(client):
    client.add_cog(OnGuildJoin(client))
    print('OnGuildJoin')
