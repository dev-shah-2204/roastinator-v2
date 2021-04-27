import random

import discord
from discord.ext import commands, tasks
from discord.ext.commands import BucketType, CommandOnCooldown

from .. import hex_colors  # Had to copy the hex_colors file from the main directory


class BotStats(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name = 'ping', help = "Bot's ping/latency")
    async def ping(self, ctx):
        em = discord.Embed(color = random.choice(hex_colors.colors))
        em.add_field(name = "Pong!", value = f"{round(self.client.latency*1000)}ms")# *1000 to change it into ms

        await ctx.send(embed = em)


    @commands.command(name = 'updates', help = "Shows latest updates")
    async def updates(self, ctx):
        await ctx.send("""
```yml
New command: Lock
New command: Unlock
New command: RoleInfo

Bug fixes:
+Clear command 
| '<user> has deleted <amount> messages' message will be auto-deleted
```
""")

    @commands.command(name = 'invite', help = 'Invite the bot to your server')
    @commands.cooldown(1, 10,  BucketType.guild)
    async def invite(self, ctx):
        InviteEmbed = discord.Embed(
            title = 'Thank you for inviting me', 
            description = f"[Click here](https://discord.com/api/oauth2/authorize?client_id={self.client.user.id}&permissions=268823638&scope=bot)")

        await ctx.send(embed = InviteEmbed)

def setup(client):
    client.add_cog(BotStats(client))
    print("BotStats Command cog loaded")
