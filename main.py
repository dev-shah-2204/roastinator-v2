"""
To know more about the discord library in python, I recommend https://discordpy.readthedocs.io/en/latest
"""
#Imports
import discord
import os

from discord.ext import commands

class Bot():
    prefix = commands.when_mentioned_or('-')
    t_prefix = '>'
    token = os.environ.get('token')

#Defining our bot (client)
client = commands.Bot(command_prefix = Bot.t_prefix, intents = discord.Intents.all(), case_insensitive = True)
client.remove_command('help')


#Cogs list
event_cog_list = [
    'on_message',
    'on_ready'
]

cmd_cog_list = [
    'botStats.ping',
    'developer.cogs',
    'developer.modmail',
    'help',
    'moderation.ban',
    'moderation.clean',
    'moderation.clear',
    'moderation.kick',
    'moderation.lock_unlock',
    'moderation.mute_unmute',
    'utility.avatar',
    'utility.editsnipe',
    'utility.python_cmd',
    'utility.role_info',
    'utility.serverinfo',
    'utility.snipe',
    'utility.user_info'
]

#Loading cogs
for event_cog in event_cog_list:
    if __name__ == '__main__':
        client.load_extension(f"cogs.events.{event_cog}")

for cmd_cog in cmd_cog_list:
    if __name__ == '__main__':
        client.load_extension(f"cogs.commands.{cmd_cog}")

client.run(Bot.token)
