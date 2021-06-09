"""
https://discordpy.readthedocs.io/en/latest
will help you out with most of your problems
"""
import discord
import os

from database_functions import *
from cleardb_db import database
from discord.ext import commands

db = database.cursor()

def get_prefix(client, message):
    db.execute(f"SELECT prefix FROM Prefix WHERE guild = '{str(message.guild.id)}'")
    for row in db:
        final = str(row).strip("('',)") #It's a tuple in the database, with a comma after the prefix string.
        return final


class Bot():
    prefix = commands.when_mentioned_or(get_prefix)
    t_prefix = '>' #Different prefix that I use when I host the bot from my PC for testing a new command or fixing bugs.
    token = os.environ.get('token')


#Defining our bot (client)
client = commands.Bot(command_prefix = Bot.prefix, intents = discord.Intents.all(), case_insensitive = True)
client.remove_command('help')


#Cogs list
event_cog_list = (
    'on_command_error',
    'on_guild_join',
    'on_message',
    'on_ready'
)

passive_cog_list = (
    'nqn'
)

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
    'utility.prefix',
    'utility.python_cmd',
    'utility.role_info',
    'utility.serverinfo',
    'utility.snipe',
    'utility.user_info',
    'utility.urban'
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

client.run(Bot.token)
