"""
https://discordpy.readthedocs.io/en/latest
will help you out with most of your problems
"""
import discord
import os
import json

from db import *
from discord.ext import commands


def get_prefix(_client, message):
    """
    Function to get prefix for a guild
    """
    with open('prefix.json', 'r') as f:
        cache = json.load(f)

    guild = str(message.guild.id)
    if guild in cache:  # We don't want to call the database every single time
        prefix = commands.when_mentioned_or(cache[guild])(_client, message)
        return prefix

    else:
        db.execute(f"SELECT prefix FROM Prefix WHERE guild = {str(message.guild.id)}")
        prefix = db.fetchone()
        cache[guild] = prefix[0]  # So that it gets stored in the cache
        with open('prefix.json', 'w') as f:
            json.dump(cache, f)

        return commands.when_mentioned_or(prefix[0])(_client, message)


"""
+--------------------------------+
| Making the commands.Bot object |
+--------------------------------+
"""

client = commands.Bot(
    command_prefix=get_prefix,
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
    'ignore_people',
    'modmail',
    'on_command_error',
    'on_guild_join',
    'on_guild_remove',
    'on_member_join',
    'on_mention',
    'on_ready',
    'starboard',
    'nqn'
)

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

"""
+--------+
|  COGS  |
+--------+
"""

for event_cog in event_cog_list:
    if __name__ == '__main__':
        try:
            client.load_extension(f"cogs.events.{event_cog}")
        except Exception as e:
            print(e)

for command_cog in cmd_cog_list:
    if __name__ == '__main__':
        try:
            client.load_extension(f"cogs.commands.{command_cog}")
        except Exception as e:
            print(e)


client.load_extension("jishaku")  # pip install jishaku
#client.run(os.environ.get('token'))
client.run(os.environ.get('token'))
