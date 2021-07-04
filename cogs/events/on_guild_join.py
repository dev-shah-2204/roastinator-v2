import discord
import mysql.connector

from discord.ext import commands
from db import *



class OnGuildJoin(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        db.execute(f"INSERT INTO Prefix(guild, prefix) VALUES ('{guild.id}','-')")
        db.execute(f"INSERT INTO AutoMod(guild, _status) VALUES ('{guild.id}','enabled')")
        database.commit()


def setup(client):
    client.add_cog(OnGuildJoin(client))
    print('OnGuildJoin')
