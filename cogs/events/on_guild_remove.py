import discord
import mysql.connector

from discord.ext import commands
from db import *


class OnGuildRemove(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        db.execute(f"DELETE FROM Prefix WHERE guild = '{guild.id}'")
        db.execute(f"DELETE FROM AutoMod WHERE guild = '{guild.id}'")
        database.commit()


def setup(client):
    client.add_cog(OnGuildRemove(client))
    print('OnGuildRemove')
