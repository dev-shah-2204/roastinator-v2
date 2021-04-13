import discord
import random

from discord.ext import commands
from discord.ext.commands import CommandOnCooldown, BucketType
from .. import hex_colors


colors = hex_colors.colors

class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name = 'clear', aliases = ['delete','purge','prune'], help = 'Mass delete messages', usage = '<number of messages>')
    @commands.has_permissions(manage_messages = True)
    async def clear(self, ctx, amount = 1):
        if amount <= 0: #people do use -clear -1 and all xD
            await ctx.send("I'm kinda confused")
            return

        if amount > 200:
            await ctx.send("Now, I could do that, but discord doesn't like it when I do that.")
            return

        await ctx.channel.purge(limit = amount+1) #Amount +1 because the command message is also included
        await ctx.send(f"**{ctx.author.name}** deleted {amount} messages", delete_after = 10)


    @commands.command(name = 'kick', help = 'Kick a member from the server', usage = '<member> [reason]')
    @commands.has_permissions(kick_members = True)
    @commands.bot_has_permissions(kick_members = True)
    async def kick(self, ctx, member:discord.Member, *, reason = None): #Default reason is "No reason provided"
        if reason == None:
            await ctx.send("You need to provide a reason")

        if member == self.client.user: #If  the 'member' is the bot
            await ctx.send(":(")
            return

        if member == ctx.author: #If the 'member' is the person who invoked the command
            await ctx.send("Why do you wanna kick your self?")
            return

        #Checking if the other person has a higher role
        if member.top_role.position >= ctx.author.top_role.position:
            await ctx.send(f"{member.mention} has a higher role than you/same role as you. You cannot kick them")
            return

        try:
            await member.kick(reason = reason)
        except:
            await ctx.send(f"{member} has a higher role than me, I can't kick them")
            return


        em = discord.Embed(color = random.choice(colors))
        em.set_author(name = f"{ctx.author} kicked {member}", icon_url = ctx.author.avatar_url)
        em.set_thumbnail(url = member.avatar_url)
        em.add_field(name = 'Reason:', value = reason)

        await ctx.send(embed = em)

    
    @commands.command(name = 'ban', help = 'Ban a member from the server', usage = '<member> <reason>')
    @commands.has_permissions(ban_members = True)
    @commands.bot_has_permissions(ban_members = True)
    async def ban(self, ctx, member:discord.Member, *, reason = None): #Default reason is "No reason provided"
        if reason == None:
            await ctx.send("You need to provide a reason")

        if member == self.client.user: #If  the 'member' is the bot
            await ctx.send(":(")
            return

        if member == ctx.author: #If the 'member' is the person who invoked the command
            await ctx.send("Why do you wanna ban your self?")
            return

        #Checking if the other person has a higher role
        if member.top_role.position >= ctx.author.top_role.position:
            await ctx.send(f"{member.mention} has a higher role than you/same role as you. You cannot ban them")
            return


        try:
            await member.ban(reason = reason)
        except:
            await ctx.send(f"{member}'s role is higher than me, I cant ban them")
            return

        em = discord.Embed(color = random.choice(colors))
        em.set_author(name = f"{ctx.author} banned {member}", icon_url = ctx.author.avatar_url)
        em.set_thumbnail(url = member.avatar_url)
        em.add_field(name = 'Reason:', value = reason)

        await ctx.send(embed = em)


    @commands.command(name = 'mute', aliases = ['stfu'], help = 'Mute people', usage = '<member>')
    @commands.has_permissions(manage_roles = True)
    async def mute(self, ctx, member:discord.Member, *, reason = "No reason provided"):
        

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


    @commands.command(name = 'unmute', aliases = ['unstfu'], help = 'Unmute muted people', usage = '<member>')
    @commands.has_permissions(manage_roles = True)
    async def unmute(self, ctx, member:discord.Member, *, reason = "No reason provided"):
        try: 
            role = discord.utils.get(ctx.guild.roles, name = 'Muted')
        except:
            await ctx.send(f"Your server doesn't have a 'Muted' role, I highly doubt {member} is muted")
            await ctx.guild.create_role(name = 'Muted', permissions = permissions, reason = 'For mute command') #Making new role
            
            for channel in ctx.guild.channels: #Changing the permission for the Muted role in all channels
                overwrite = channel.overwrites_for(role)
                overwrite.send_messages = False

                await channel.set_permissions(role, overwrite = overwrite)

            
        if role not in member.roles:
            await ctx.send(f"{member} isn't even muted")
            return

        else:
            await member.remove_roles(role, reason = f'Unmute command ran by {ctx.author}')

            em = discord.Embed(
                        title = f"{ctx.author} muted {member}",
                        description = f"Reason:\n{reason}",
                        color = hex_colors.m_red
                        )
            em.set_thumbnail(url = member.avatar_url)

            await ctx.send(embed = em)


    @commands.command(name = 'lock', aliases = ['lc','lockchannel'], help = 'Locks a channel')
    @commands.has_permissions(manage_channels = True)
    @commands.bot_has_permissions(manage_channels = True)
    async def lock_channel(self, ctx, channel:discord.TextChannel = None):
        #The code in this command is basically plain english, quite self explanatory 
        if channel == None:
            channel = ctx.channel

        if channel not in ctx.guild.channels:
            await ctx.send("Hmm, seems like that channel isn't from this server... Don't go around doing shady stuff like that.")
            return

        if type(channel) == discord.VoiceChannel:
            await ctx.send("That command only works for text channels..")
            return

        await ctx.send("Locking the channel. There's a high chance that I will get muted too and won't be able to send the confirmation message")
        await channel.set_permissions(ctx.guild.default_role, send_messages = False)
        await ctx.send("Apparently I didn't get muted. Locked the channel")

    
    @commands.command(name = 'unlock', aliases = ['ulc','unlockchannel'], help = 'Unlocks a channel')
    @commands.has_permissions(manage_channels = True)
    @commands.bot_has_permissions(manage_channels = True)
    async def unlock_channel(self, ctx, channel:discord.TextChannel = None):
        #The code in this command is basically plain english, quite self explanatory 
        if channel == None:
            channel = ctx.channel

        if channel not in ctx.guild.channels:
            await ctx.send("Hmm, seems like that channel isn't from this server... Don't go around doing shady stuff like that.")
            return

        if type(channel) == discord.VoiceChannel:
            await ctx.send("That command only works for text channels..")
            return

        await channel.set_permissions(ctx.guild.default_role, send_messages = True)
        await ctx.send("Unlocked the channel")
      
        

def setup(client):
    client.add_cog(Moderation(client))
    print("Moderation Command cog loaded")
