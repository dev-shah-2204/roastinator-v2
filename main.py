"""
https://discordpy.readthedocs.io/en/latest
will help you out with most of your problems
"""
import discord
import os

from discord.ext import commands

testing = False #If set to true, sends error from console in discord.

class Bot():
    prefix = '-'
    t_prefix = '>' #Different prefix that I use when I host the bot from my PC for testing a new command or fixing bugs.
    token = os.environ.get('token')

#Defining our bot (client)
client = commands.Bot(command_prefix = Bot.prefix, intents = discord.Intents.all(), case_insensitive = True)
client.remove_command('help')


#Cogs list
event_cog_list = (
    'on_command_error',
    'on_message',
    'on_ready'
)

passive_cog_list = [
    'nqn'
] #This is a list instead of a tuple because the for loop detects nqn as n, q, n when loading the cog

cmd_cog_list = (
    'botStats.invite',
    'botStats.ping',
    'developer.cogs',
    'developer.modmail',
    'fun.meme',
    'fun.say',
    'games.cointoss',
    'games.rockpaperscissors',
    'help',
    'moderation.ban',
    'moderation.clean',
    'moderation.clear',
    'moderation.kick',
    'moderation.lock_unlock',
    'moderation.mute_unmute',
    'moderation.nuke',
    'moderation.temp_mute',
    'utility.avatar',
    'utility.editsnipe',
    'utility.embed',
    'utility.python_cmd',
    'utility.role_info',
    'utility.serverinfo',
    'utility.snipe',
    'utility.urban',
    'utility.user_info'
)

#Loading cogs
for event_cog in event_cog_list:
    if __name__ == '__main__':
        client.load_extension(f"cogs.events.{event_cog}")

for cmd_cog in cmd_cog_list:
    if __name__ == '__main__':
        client.load_extension(f"cogs.commands.{cmd_cog}")

for psv_cog in passive_cog_list:
    if __name__ == '__main__':
        client.load_extension(f"cogs.passive.{psv_cog}")

if testing == True:
    client.load_extension("cogs.events.error_sender")

client.run(Bot.token)
