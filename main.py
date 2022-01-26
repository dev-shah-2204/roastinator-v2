import os
import discord

from dotenv import load_dotenv
from utils import checks
from bot import Roastinator

load_dotenv()

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
    if isinstance(coro, discord.ext.commands.context.Context) or isinstance(coro, discord.ext.commands.Context):
        command_blacklist = checks.get_command_blacklist()

        if str(coro.author.id) in command_blacklist:
            await coro.send("You've been blacklisted from using this bot. If you thing this is a mistake, contact StatTrakDiamondSword#5493. If they have blocked you, then there's nothing that can be done.")
            raise Exception(f"{coro.author} ({coro.author.id}) - blacklisted user - tried using {coro.command}")

bot.run(os.getenv('token'))
