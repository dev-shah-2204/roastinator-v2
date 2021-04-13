import os
import random
import discord
import pytz

from datetime import datetime
from discord.ext import commands
from discord.ext.commands import BucketType, CommandOnCooldown
from .. import hex_colors

del_msg = {}
edit_msg = {}

class Utility(commands.Cog):
    def __init__(self, client):
        self.client = client

    #Events
    @commands.Cog.listener()
    async def on_message_delete(self, message):

        del_msg[str(message.channel.id)] = {}
        del_msg[str(message.channel.id)]['content'] = message.content
        del_msg[str(message.channel.id)]['author'] = message.author
        del_msg[str(message.channel.id)]['time'] = datetime.now(pytz.utc) #This will be used for the timestamp

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        edit_msg[str(before.channel.id)] = {}

        edit_msg[str(before.channel.id)]['before'] = before.content
        edit_msg[str(before.channel.id)]['after'] = after.content
        edit_msg[str(before.channel.id)]['author'] = before.author
        edit_msg[str(before.channel.id)]['time'] = datetime.now(pytz.utc) #This will be used for the timestamp


    #Commands
    @commands.command(name = 'snipe', help = 'Check the last deleted message in the channel', usage = '')
    async def snipe(self, ctx):
        try:
            msg_content = del_msg[str(ctx.channel.id)]['content']
            if msg_content == '': #If the message had no text, it means that it had an attachment. Since the message is deleted, we can't retrieve that.
                msg_content = "There was an image or an embed in the deleted message that couldn't be loaded"

            em = discord.Embed(description = msg_content, color = random.choice(hex_colors.colors), timestamp = del_msg[str(ctx.channel.id)]['time'])
            em.set_author(name = f"{del_msg[str(ctx.channel.id)]['author']} said:", icon_url = del_msg[str(ctx.channel.id)]['author'].avatar_url)

            await ctx.send(embed = em)
        except:
            await ctx.send("There are no recently deleted messages")


    @commands.command(name = 'editsnipe', aliases = ['es'], help = 'Check the last edited message in the channel', usage = '')
    async def editsnipe(self, ctx):
        try:

            em = discord.Embed(color = random.choice(hex_colors.colors), timestamp = edit_msg[str(ctx.channel.id)]['time'])
            em.set_author(name = f"{edit_msg[str(ctx.channel.id)]['author']} said:", icon_url = edit_msg[str(ctx.channel.id)]['author'].avatar_url)
            em.add_field(name = 'Before', value = edit_msg[str(ctx.channel.id)]['before'], inline = False) #If the embed has 2 fields, using inline = False only once is enough)
            em.add_field(name = 'After', value = edit_msg[str(ctx.channel.id)]['after'])

            await ctx.send(embed = em)

        except:
            await ctx.send("There are no recently edited messages")

def setup(client):
    client.add_cog(Utility(client))
    print("Snipe Command cog loaded")
