import discord
import hex_colors

from discord.ext import commands


class Nuke(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command(name='nuke', help='Deletes the channel and makes a copy of it')
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(administrator=True)
    async def nuke(self, ctx):
        existing_channel = discord.TextChannel(ctx.channel)

        new_channel = await existing_channel.clone(reason=f'Original was nuked by {ctx.author}') #Reason to be registered in the audit log
        await new_channel.edit(position=existing_channel.position)
        try:
            await ctx.channel.delete()
        except discord.Forbidden:
            await ctx.send("I couldn't delete the channel, maybe this is a community updates channel?") #Channels that are set for community updates cannot be deleted without transferring the community updates to another channel

        em = discord.Embed(
                    title='This channel got nuked!',
                    description='Who did this? Check Audit Log',
                    color=hex_colors.m_red)

        await new_channel.send(embed=em)


def setup(client):
    client.add_cog(Nuke(client))
    print('Nuke')
