import discord
import random 
import hex_colors

from db import database
from discord.ext import commands 

db = database.cursor()

class OnMention(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.content == f'<@!{self.client.user.id}>' or msg.content == f'<@{self.client.user.id}>':
            #If the bot is mentioned
            db.execute(f"SELECT prefix FROM Prefix WHERE guild = '{msg.guild.id}'")
            for row in db:
                prefix = row
            
            prefix = str(prefix)
            prefix = prefix.replace("('",'') #complex
            prefix = prefix.replace("',)",'') #very complex mmmhm
            em = discord.Embed(
                title=f'My prefix for this server is `{prefix}`',
                color=random.choice(hex_colors.colors)
            )
            await msg.channel.send(embed=em)


def setup(client):
    client.add_cog(OnMention(client))
    print('OnMention')