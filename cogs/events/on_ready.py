"""
Having trouble figuring out cogs? Check the on_message.py file
"""
import discord

from discord.ext import commands
from pytz import timezone
from datetime import datetime

class onReady(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('--------------')
        print('All cogs loaded')
        #Since I host the bot on heroku, I'd like to know in the logs when the bot started/restarted in my own timezone
        print("Date:", datetime.now(timezone('Asia/Kolkata')).strftime('%d = %m - %Y'))
        print("Time:", datetime.now(timezone('Asia/Kolkata')).strftime('%H:%M'))

def setup(client):
    client.add_cog(onReady(client))
    print('onReady')
