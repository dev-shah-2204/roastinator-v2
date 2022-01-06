import os
import discord

from utils import checks
from bot import Roastinator


bot = Roastinator()
bot.remove_command('help')

cogs = [
    'basic',
    'developer',
    'error_handler',
    'events',
    'fun',
    'games',
    'help',
    'moderation',
    'utility'
]

for cog in cogs:
    bot.load_extension(f'cogs.{cog}')

bot.load_extension('jishaku')

@bot.before_invoke
async def before_invoke(coro):
    """
    This isn't working properly. Please fix if you can
    """
    if isinstance(coro, discord.ext.commands.context.Context) or isinstance(coro, discord.ext.commands.Context):
        command_blacklist = checks.get_command_blacklist()

        if str(coro.author.id) in command_blacklist:
            return

bot.run(os.getenv('token'))
