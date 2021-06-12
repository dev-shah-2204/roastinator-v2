import discord
from discord.ext import commands


class ErrorSender(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await ctx.send(f"```{error}```")

def setup(client):
    client.add_cog(ErrorSender(client))
    print("ErrorSender")
