"""
https://discordpy.readthedocs.io/en/latest
will help you out with most of your problems
"""
import discord
import os

from discord.ext import commands

testing = False #If set to true, sends error from console in discord.

class Bot():
    prefix = commands.when_mentioned_or('-')
    t_prefix = '>' #Different prefix that I use when I host the bot from my PC for testing a new command or fixing bugs.
    token = os.environ.get('token')

#Defining our bot (client)
client = commands.Bot(command_prefix = Bot.prefix, intents = discord.Intents.all(), case_insensitive = True) 
#You'll have to apply for intents when your bot gets verified
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
    'fun.wholesome',
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
    'utility.reddit',
    'utility.role_info',
    'utility.serverinfo',
    'utility.snipe',
    'utility.steal_emoji',
    'utility.urban',
    'utility.user_info'
)

#Loading cogs
for event_cog in event_cog_list:
    if __name__ == '__main__':
        client.load_extension(f"cogs.events.{event_cog}")

for command_cog in cmd_cog_list:
    if __name__ == '__main__':
        client.load_extension(f"cogs.commands.{command_cog}")

for passive_cog in passive_cog_list:
    if __name__ == '__main__':
        client.load_extension(f"cogs.passive.{passive_cog}")


"""
The following cog loading method is easiser since you dont have to make a big tuple, but if you don't want to load some cogs,
it can pose as a problem. And making the cog tuple isn't difficult. Over time, it will get big, sure, but that doesn't matter.

Make a cog, add to the tuple. Not that difficult.
"""
# for event_cog in os.listdir('./cogs/events'):
#     if event_cog.endswith('.py'):
#         client.load_extension(f"cogs.events.{event_cog[:-3]}")

# for folder in os.listdir('./cogs/commands'):
#     print(folder)
#     for cmd_cog in os.listdir(f'./cogs/commands/{folder}'):
#         if cmd_cog.endswith('.py'):
#             client.load_extension(f"cogs.commands.{folder}.{cmd_cog[:-3]}")

# client.load_extension(f"cogs.passive.nqn")


if testing == True:
    client.load_extension("cogs.events.error_sender")

client.run(Bot.token)
