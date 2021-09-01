import discord 
import json

from discord.ext import commands 
from db import *


class AutoModEvent(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def get_status(self, guild):
        with open('automod.json', 'r') as f:
            cache = json.load(f)
        guild = str(guild)

        if guild not in cache:
            db.execute(f"SELECT _status FROM automod WHERE guild = '{guild}'")
            status = await get_data(db=db)
            if status is not None:
                db.execute(f"SELECT * FROM am_{guild}")
                blacklist = db.fetchall()
                lst = []
                for word in blacklist:
                    lst.append(word[0])

                cache[str(guild)] = {}
                cache[str(guild)]['status'] = 'enabled'
                cache[str(guild)]['blacklist'] = lst

                with open('automod.json', 'w') as f:
                    json.dump(cache, f)

            else:
                cache[str(guild)] = {}
                cache[str(guild)]['status'] = 'disabled'
                cache[str(guild)]['blacklist'] = []

                with open('automod.json', 'w') as f:
                    json.dump(cache, f)

        else:
            status = cache[str(guild)]['status']

        return status


    async def get_blacklist(self, guild):
        with open('automod.json', 'r') as f:
            cache = json.load(f)

        blacklist = []

        if guild not in cache:
            db.execute(f"SELECT * FROM am_{guild}")
            lst = db.fetchall()
            for word in lst:
                blacklist.append(word[0]) #word is a tuple

            cache[str(guild)]['blacklist'] = blacklist

            with open('automod.json', 'w') as f:
                json.dump(cache, f)
        else:
            blacklist = cache[str(guild)]['blacklist']

        return blacklist


    @commands.Cog.listener()
    async def on_message(self, msg):
        if not msg.author.bot and not isinstance(msg.channel, discord.DMChannel):
            status = await self.get_status(msg.guild.id)
            if status == 'enabled':
                member = msg.guild.get_member(msg.author.id)
                if member is not None:
                    if not member.guild_permissions.manage_messages: #If message author doesn't have manage_messages permission
                        blacklist = await self.get_blacklist(str(msg.guild.id))

                        for word in blacklist:
                            if word.lower() in msg.content.lower():
                                await msg.delete()
                                try:
                                    await msg.author.send(f"Hey! That word is not allowed in {msg.guild.name}")
                                except:
                                    pass
                                break


def setup(client):
    client.add_cog(AutoModEvent(client))
    print("AutoModEvent")
