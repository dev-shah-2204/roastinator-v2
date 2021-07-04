"""
Got help on this one from Black Tooth's dev
https://blacktooth-bot.com
"""
import discord

from discord.ext import commands
from cache import am as cache 
class Say(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='say', help='Make the bot say stuff')
    async def say(self, ctx, *, message):
        if 'https://' in message or 'http://' in message:
            await ctx.send("I'm afraid I can't send links.")
            return
        if 'discord.gg' in message:
            await ctx.send("I'm afraid I can't send invite links")
            return 

        if str(ctx.guild.id) in cache:
            blacklist = cache[str(ctx.guild.id)]
            for word in blacklist:
                if word.lower() in message.lower():
                    await ctx.send(f"Ayo {ctx.author.mention}, don't make me say blacklisted words!")
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
