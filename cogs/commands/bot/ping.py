"""
Having trouble figuring out cogs? Check the on_message.py file
"""
import discord, random
import hex_colors

from discord.ext import commands

class Ping(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name = 'ping', help = "Shows the bot's ping/latency")
    async def ping(self, ctx):
        em = discord.Embed(
            title = 'Pong!',
            description = f"{round(self.client.latency*1000)}ms", #*1000 to convert to milliseconds
            color = random.choice(hex_colors.colors)
            ) #Don't know what embeds are? They're really cool.

        await ctx.send(embed = em) #ctx stands for context. 'embed = ' to let the bot know that em is an embed. else it would just send the 'em' object as a string

def setup(client):
    client.add_cog(Ping(client))
    print('Ping')
