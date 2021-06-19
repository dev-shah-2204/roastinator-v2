import discord
import hex_colors

from discord.ext import commands

class Nuke(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name = 'nuke', help = 'Deletes the channel and makes a copy of it')
    @commands.has_permissions(manage_channels = True)
    @commands.bot_has_permissions(manage_channels = True)
    async def nuke(self, ctx):
        existing_channel = ctx.channel
        pos = existing_channel.position
        
        new_channel = await existing_channel.clone(reason = f'Original was nuked by {ctx.author}') #Reason to be registered in the audit log
        await new_channel.edit(position = pos)
        await ctx.channel.delete()

        em = discord.Embed(
                    title = 'This channel got nuked!',
                    description = 'Who did this? Check Audit Log',
                    color = hex_colors.m_red)

        await new_channel.send(embed = em)

def setup(client):
    client.add_cog(Nuke(client))
    print('Nuke')
