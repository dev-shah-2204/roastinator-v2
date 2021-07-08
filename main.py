"""
https://discordpy.readthedocs.io/en/latest
will help you out with most of your problems
"""
import discord
import os

from cache import prefix_cache
from db import *
from discord.ext import commands


def get_prefix(_client, message):
    cache = prefix_cache
    guild = str(message.guild.id)
    if guild in cache:  # We don't want to call the database every single time
        prefix = cache[guild]
        return prefix

    else:
        db.execute(f"SELECT prefix FROM Prefix WHERE guild = {str(message.guild.id)}")
        for row in db:
            prefix = row[0]  # row is a tuple
            cache[guild] = prefix  # So that it gets stored in the cache
            return prefix


token = os.environ.get('token')

# Defining our bot (client)
client = commands.Bot(
    command_prefix='>',
    intents=discord.Intents.all(),
    case_insensitive=True,
    allowed_mentions=discord.AllowedMentions(everyone=False),
    owner_id=416979084099321866
)
client.remove_command('help')

# Cogs list
event_cog_list = (
    'auto_mod',
    'fix_prefix',
    'modmail',
    'on_command_error',
    'on_guild_join',
    'on_guild_remove',
    'on_member_join',
    'on_mention',
    'on_ready',
    'starboard'
)

passive_cog_list = [
    'nqn'
]

cmd_cog_list = (
    'bot.invite',
    'bot.ping',
    'developer.cogs',
    'developer.modmail',
    'developer.modmail_reply',
    'fun.bonk',
    'fun.cursed',
    'fun.dadjoke',
    'fun.meme',
    'fun.roast',
    'fun.say',
    'fun.wholesome',
    'games.cointoss',
    'games.rockpaperscissors',
    'help',
    'moderation.automod',
    'moderation.autorole',
    'moderation.ban',
    'moderation.clean',
    'moderation.clear',
    'moderation.kick',
    'moderation.lock_unlock',
    'moderation.mute_unmute',
    'moderation.nuke',
    'moderation.softban',
    'moderation.temp_mute',
    'utility.avatar',
    'utility.csgo',
    'utility.editsnipe',
    'utility.embed',
    'utility.enlarge_emoji',
    'utility.prefix',
    'utility.python_cmd',
    'utility.reddit',
    'utility.role_info',
    'utility.serverinfo',
    'utility.snipe',
    'utility.starboard',
    'utility.steal_emoji',
    'utility.urban',
    'utility.user_info'
)

# Loading cogs
for event_cog in event_cog_list:
    if __name__ == '__main__':
        client.load_extension(f"cogs.events.{event_cog}")

for command_cog in cmd_cog_list:
    if __name__ == '__main__':
        client.load_extension(f"cogs.commands.{command_cog}")

for passive_cog in passive_cog_list:
    if __name__ == '__main__':
        client.load_extension(f"cogs.passive.{passive_cog}")

client.load_extension("jishaku")

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

client.run(token)
