import discord

from discord.ext import commands
from discord.ext.commands import CommandOnCooldown, BucketType


class LockUnlock(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='lock', aliases=['lockchannel'], help='Locks a channel')
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def lock_channel(self, ctx, channel:discord.TextChannel=None):
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
        await channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await ctx.send("Apparently I didn't get muted. Locked the channel")


    @commands.command(name='unlock', aliases=['ulc','unlockchannel'], help='Unlocks a channel')
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def unlock_channel(self, ctx, channel:discord.TextChannel=None):
        #The code in this command is basically plain english, quite self explanatory
        if channel == None:
            channel = ctx.channel

        if channel not in ctx.guild.channels:
            await ctx.send("Hmm, seems like that channel isn't from this server... Don't go around doing shady stuff like that.")
            return

        if type(channel) == discord.VoiceChannel:
            await ctx.send("That command only works for text channels..")
            return

        await channel.set_permissions(ctx.guild.default_role, send_messages=None)
        await ctx.send("Unlocked the channel")

def setup(client):
    client.add_cog(LockUnlock(client))
    print('LockUnlock')
