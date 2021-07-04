import discord
import mysql.connector

from discord.ext import commands
from db import *



class OnGuildJoin(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        for channel in guild.text_channels:
            if guild.me.guild_permissions.send_messages:
                em = discord.Embed(
                    title='Hey there!',
                    description='Thanks for inviting me to your server.\nMy prefix is `-`. If you wish to change it, use the prefix command.',
                    color=0x60FF60
                )
                em.add_field(
                    name='Example usage:',
                    value=f'{self.client.user.mention} prefix `newPrefix`\nor\n-prefix `newPrefix`'
                )
                await channel.send(embed=em)
                break
        db.execute(f"INSERT INTO Prefix(guild, prefix) VALUES ('{guild.id}','-')")
        db.execute(f"INSERT INTO AutoMod(guild, _status) VALUES ('{guild.id}','enabled')")
        database.commit()


def setup(client):
    client.add_cog(OnGuildJoin(client))
    print('OnGuildJoin')
