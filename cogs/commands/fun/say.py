"""
Got help on this one from Black Tooth's dev
https://blacktooth-bot.com
"""
import discord

from discord.ext import commands

class Say(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='say', help='Make the bot say stuff')
    async def say(self, ctx, *, message):
        if 'https://' in message or 'http://' in message:
            await ctx.send("I'm afraid I can't send links.")
            return
        await ctx.message.delete()
        await ctx.send(f"{ctx.author.mention} said {message}", allowed_mentions=discord.AllowedMentions(
            everyone=False,
            roles=False,
            users=False
            )
        )


def setup(client):
    client.add_cog(Say(client))
    print('Say')
