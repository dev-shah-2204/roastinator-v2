import discord
import hex_colors

from asyncio import sleep
from discord.ext import commands

class TempMute(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name = 'tempmute', aliases = ['tempstfu'], help = 'Temporarily mute people (Mode is `s`, `m`, `h` or `d`)')
    @commands.has_permissions(manage_roles = True)
    @commands.bot_has_permissions(manage_roles = True)
    async def mute(self, ctx, member:discord.Member, time:int, mode = 'm', *, reason = "No reason provided"):
        role = discord.utils.get(ctx.guild.roles, name = 'Muted') #Searching if the role already exists (If some other bot made it)
        permissions = discord.Permissions(send_messages = False) #Permission for new role (in case role doesn't exist)

        if not role in ctx.guild.roles:
            await ctx.send("Hold on, making a 'Muted' role. Don't worry, this process won't take place every time you run this command")
            await ctx.guild.create_role(name = 'Muted', permissions = permissions, reason = 'For mute command') #Making new role

        role = discord.utils.get(ctx.guild.roles, name = 'Muted') #The old role variable might have returned None
        await member.add_roles(role, reason = f"{ctx.author} ran the mute command")

        em = discord.Embed(
                        title = f"{ctx.author} muted {member}",
                        description = f"Reason:\n{reason}",
                        color = hex_colors.m_red
                        )
        em.set_thumbnail(url = member.avatar_url)

        await ctx.send(embed = em)

        for channel in ctx.guild.channels: #Changing the permission for the Muted role in all channels
                overwrite = channel.overwrites_for(role)
                overwrite.send_messages = False

                await channel.set_permissions(role, overwrite = overwrite)

        multiplier = 1 #If we put 0, and someone uses the command wrong, problems might occur.

        if mode == 's' or mode == 'seconds' or mode == 'second':
            multiplier = 1
        if mode == 'm' or mode == 'minutes' or mode == 'minute':
            multiplier = 60
        if mode == 'h' or mode == 'hours' or mode == 'hour':
            multiplier = 60*60
        if mode == 'd' or mode == 'days' or mode == 'day':
            multiplier = 60*60*24

        await sleep(time*multiplier)
        await member.remove_roles(role, reason = f"Temporary mute is over. Responsible moderator: {ctx.author}")

def setup(client):
    client.add_cog(TempMute(client))
    print("TempMute")
