import json 
import discord

from discord.ext import commands
from utils import checks
from db import *

def get_prefix(bot, message):
    prefix = checks.get_server_prefix(message)
    return commands.when_mentioned_or(prefix)(bot, message)


class Roastinator(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(
            command_prefix = get_prefix,
            intents=discord.Intents.all(),
            case_insensitive=True,
            allowed_mentions=discord.AllowedMentions(everyone=False),  # Set this according to your own preference
            owner_id=416979084099321866  # Enter your discord ID here
        )


if __name__ == "__main__":
    raise RuntimeError("Make sure you're running the main.py file and not the bot.py file")
    exit()
