import discord
import hex_colors
import asyncio

from discord.ext import commands


class Nuke(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command(name='nuke', help='Deletes the channel and makes a copy of it')
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(administrator=True)
    async def nuke(self, ctx, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.channel 
            
        existing_channel = ctx.channel

        new_channel = await existing_channel.clone(reason=f'Original was nuked by {ctx.author}') #Reason to be registered in the audit log
        await new_channel.edit(position=existing_channel.position)
        
        def check(message: discord.Message) -> bool:
            return message.author == ctx.author
        
        await ctx.send("Type `confirm` if you wish to proceed with nuking the channel. Type `cancel` if you do not wish to proceed with nuking the channel.")
        
        try:
            message = await self.client.wait_for('message', timeout=10, check=check)
            
            if message.content.lower() == "cancel":
                await ctx.send("Okay, cancelled.")
                return 
            
            elif message.content.lower() == "confirm":
                try:
                    await ctx.channel.delete()
                except discord.Forbidden:
                    await ctx.send("I couldn't delete the channel, maybe this is a community updates channel?") #Channels that are set for community updates cannot be deleted without transferring the community updates to another channel

                em = discord.Embed(
                            title='This channel got nuked!',
                            description='Who did this? Check Audit Log',
                            color=hex_colors.m_red)

                await new_channel.send(embed=em)
                
            else:
                await ctx.send("Invalid input. Cancelled the nuking.")
                return
            
        except asyncio.TimeoutError:
            await ctx.send("You ran out of time, run the command again")
            return
        
    

def setup(client):
    client.add_cog(Nuke(client))
    print('Nuke')
