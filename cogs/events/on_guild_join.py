import discord
import mysql.connector
from discord.ext import commands
from cleardb_db import database

db = database.cursor()

class onGuildJoin(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        """
        When the bot joins a server, we want to assign the default prefix for that server.
        """
        db.execute("INSERT INTO Prefix ('guild', 'prefix') VALUES (%s, %s)",(guild.id, '-')) #My table is called Prefix
        database.commit()


def setup(client):
    client.add_cog(onGuildJoin(client))
    print('onGuildJoin')
