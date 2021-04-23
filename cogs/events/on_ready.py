import os
import discord

from discord.ext import commands, tasks
from pytz import timezone
from datetime import datetime

class OnReady(commands.Cog, name = 'OnReady'):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('--------------------')
        print(f"Up and running!\nSigned in as {self.client.user}\nID: {self.client.user.id}")
        print("Date:", datetime.now(timezone('Asia/Kolkata')).strftime('%d - %m - %Y'))
        print("Time:", datetime.now(timezone('Asia/Kolkata')).strftime('%H:%M')) #I put Asia/Kolkata, you can put UTC or your own timezone



def setup(client):
    client.add_cog(OnReady(client))
    print('OnReady Event cog loaded')
