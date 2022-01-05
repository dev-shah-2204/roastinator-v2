import os 

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

bot.run(os.getenv('token'))
