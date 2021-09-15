import discord
import random
import asyncio
import hex_colors

from discord.ext import commands

class Cointoss(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='cointoss', aliases=['coin','coinflip','toss','flip'], help="Flip a coin") #I'm not adding a cooldown but you can
    async def coin_toss(self, ctx):
        choices = ['heads', 'tails']
        coin = random.choice(choices)

        await ctx.send('Guess `heads` or `tails`')

        def check(message: discord.Message) -> bool:
            return message.author == ctx.author #It will check if the author of the 2nd message is the person who invoked the command

        try:
            message = await self.client.wait_for('message', timeout=7, check=check)#timeout is how long the bot will wait for the second message

            if message.content.lower() not in choices:
                await ctx.send("Valid choices are `heads` and `tails`")
                return #So that the bot doesn't take any other inputs

            if message.content.lower() == coin:
                color = hex_colors.l_green
            else:
                color = hex_colors.l_red

            em = discord.Embed(title=f"Result: `{coin}`", color=color)
            await ctx.send(embed=em)


        except asyncio.TimeoutError: #If the user doesn't reply within 7 seconds i.e. the timeout we set
            await ctx.send("I can't wait forever...")


def setup(client):
    client.add_cog(Cointoss(client))
    print('Cointoss')
