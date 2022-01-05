import discord
import random 
import asyncio 

from discord.ext import commands
from discord.ext.commands import command, cooldown, BucketType
from utils import colors 


class Games(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    def check_win(self, user_choice, bot_choice):
        if user_choice == bot_choice:
            return 'draw'
        
        elif user_choice == 'rock':
            if bot_choice == 'paper':
                return 'lost'
            else:
                return 'won'
            
        elif user_choice == 'paper':
            if bot_choice == 'rock':
                return 'lost'
            else:
                return 'won'
            
        elif user_choice == 'scissors':
            if bot_choice == 'rock':
                return 'lost'
            else:
                return 'won'
            
    
    @command(name='rockpaperscissors', aliases=['rps'], help="Play a game of rock-paper-scissors with the bot")
    @cooldown(1, 3, BucketType.user)
    async def rock_paper_scissors(self, ctx, choice):
        valid_choices = ('rock', 'paper', 'scissors')
        
        choice = choice.lower()
        if choice not in valid_choices:
            await ctx.reply("Valid choices are `rock`, `paper`, `scissors`", mention_author=False)
            return 
        
        bot_choice = random.choice(valid_choices)
        check = self.check_win(choice, bot_choice)
        
        if check == 'won':
            title = 'You won!'
            color = colors.l_green
        elif check == 'lost':
            title = 'You lost. F'
            color = colors.l_red
        else:
            title = 'Draw'
            color = colors.l_yellow
            
        em = discord.Embed(
            title=title,
            color=color
        )
        em.add_field(
            name='Your choice:',
            value=choice.capitalize()
        )
        em.add_field(
            name="Bot's choice",
            value=bot_choice.capitalize(),
            inline=False
        )
        await ctx.reply(embed=em, mention_author=False)
        

    @command(name='cointoss', aliases=['coinflip', 'toss', 'flip'], help="Flip a coin")
    @cooldown(1, 3, BucketType.user)
    async def coin_toss(self, ctx, choice):
        valid_choices = ('heads', 'tails')
        choice = choice.lower()
        
        if choice not in valid_choices:
            await ctx.reply("Valid choices are `heads` and `tails`", mention_author=False)
            return
        
        coin = random.choice(valid_choices)
        
        if choice == coin:
            color = colors.l_green
        else:
            color = colors.l_red 
            
        em = discord.Embed(
            title=f"Result: `{coin}`",
            color=color
        )
        await ctx.reply(embed=em, mention_author=False)
        
        
    
def setup(bot):
    bot.add_cog(Games(bot))
    print("Games cog loaded")
