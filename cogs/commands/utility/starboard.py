import discord 
import hex_colors 

from db import *
from discord.ext import commands

class StarboardCommands(commands.Cog):
    def __init__(self, client):
        self.client = client 

    @commands.group(name = 'starboard', help = 'Commands related to starboard')
    @commands.has_permissions(manage_messages = True)
    async def starboard_commands(self, ctx):
        em = discord.Embed(
            title = "Starboard Commands",
            description = """
`channel`
`enable`
`disable`
            """,
            color = hex_colors.l_yellow)

        await ctx.send(embed = em)


def setup(client):
    client.add_cog(StarboardCommands(client))
    print('StarboardCommands')