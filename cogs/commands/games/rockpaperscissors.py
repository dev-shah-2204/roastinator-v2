import discord
import random
import asyncio
import hex_colors

from discord.ext import commands

class RockPaperScissors(commands.Cog):
    def __init__(self, client):
        self.client = client

    def check_win(self, user_choice:str, bot_choice:str): #Function to check who won, the bot or the user
        if user_choice == 'rock':
            if bot_choice == 'scissors':
                return 'won'
            if bot_choice == 'paper':
                return 'lost'

        if user_choice == 'paper':
            if bot_choice == 'rock':
                return 'won'
            if bot_choice == 'scissors':
                return 'lost'

        if user_choice == 'scissors':
            if bot_choice == 'paper':
                return 'won'
            if bot_choice == 'rock':
                return 'lost'

        if user_choice == bot_choice:
            return 'draw'

    @commands.command(name='rockpaperscissors', aliases=['rps']) #I'm not adding a cooldown but you can
    async def rock_paper_scissors(self, ctx):
        choices = ['rock','paper','scissors']
        bot_choice = random.choice(choices)

        await ctx.send('Rock, Paper or Scissors?')

        def check(message: discord.Message) -> bool:
            return message.author == ctx.author

        try:
            message = await self.client.wait_for('message', timeout=10, check=check)

            if message.content.lower() == 'scissor':
                message.content = 'scissors' #I don't wanna throw an error just because of a missing letter

            if message.content.lower() not in choices:
                await ctx.send('Valid choices are `rock`, `paper` and `scissors`')
                return

            result = self.check_win(message.content.lower(), bot_choice)

            if result == 'won':
                title = 'You won!'
                color = hex_colors.l_green

            if result == 'lost':
                title = 'You lost. F'
                color = hex_colors.l_red

            if result == 'draw':
                title = 'Draw!'
                color = hex_colors.l_yellow

            em = discord.Embed(
                title=title, 
                color=color)
            em.add_field(
                name='Your choice:', 
                value=message.content.capitalize(), 
                inline=False)
            em.add_field(
                name="Bot's choice:", 
                value=bot_choice.capitalize())

            await ctx.send(embed=em)

        except asyncio.TimeoutError:
            await ctx.send("I can't wait forever...")


def setup(client):
    client.add_cog(RockPaperScissors(client))
    print('RockPaperScissors')
