import discord, random

from discord.ext import commands
from discord.ext.commands import CommandOnCooldown, BucketType
import hex_colors

colors = hex_colors.colors

class Clear(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name = 'clear', aliases = ['delete','purge','prune'], help = 'Mass delete messages', usage = '<number of messages>')
    @commands.has_permissions(manage_messages = True)
    async def clear(self, ctx, amount = 1):
        if amount <= 0: #The number needs to be more than 0
            await ctx.send("I'm kinda confused")
            return

        if amount > 200:
            await ctx.send("Now, I could do that, but discord doesn't like it when I do that.")
            return

        await ctx.channel.purge(limit = amount+1) #Amount +1 because the command message is also included
        await ctx.send(f"**{ctx.author.name}** deleted {amount} messages", delete_after = 3)


def setup(client):
    client.add_cog(Clear(client))
    print('Clear')
