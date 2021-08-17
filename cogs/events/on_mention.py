import discord
import random 
import hex_colors
import json

from db import *
from discord.ext import commands


class OnMention(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, msg):
        with open('prefix.json', 'r') as f:
            cache = json.load(f)

        guild = str(msg.guild.id)
        if guild in cache:
            prefix = cache[guild]
        else:
            db.execute(f"SELECT prefix FROM Prefix WHERE guild = '{guild}'")
            prefix = db.fetchone()
            prefix = prefix[0]

            cache[guild] = prefix
            with open('prefix.json', 'w') as g:
                g.dump(cache, g)

        if msg.content == f'<@!{self.client.user.id}>' or msg.content == f'<@{self.client.user.id}>':
            #If the bot is mentioned
            em = discord.Embed(
                title=f'My prefix for this server is `{prefix}`',  # prefix is a tuple
                color=random.choice(hex_colors.colors)
            )
            await msg.channel.send(embed=em)


def setup(client):
    client.add_cog(OnMention(client))
    print('OnMention')
