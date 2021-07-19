import discord 

from discord.ext import commands 
from db import *
from cache import am as cache



class AutoModEvent(commands.Cog):
    def __init__(self, client):
        self.client = client 

    _status = {

    }

    async def get_status(self, guild):
        if guild not in self._status:
            db.execute(f"SELECT _status FROM automod WHERE guild = '{guild}'")
            status = await get_data(db=db)
            self._status[str(guild)] = status #Cache
        else:
            status = self._status[str(guild)] #Cache
        return status

    async def get_blacklist(self, guild):
        db.execute(f"SELECT * FROM am_{guild}")
        lst = db.fetchall()

        blacklist = []

        for word in lst:
            blacklist.append(word[0]) #word is a tuple

        cache[str(guild)] = []
        cache[str(guild)] = blacklist #Adding in cache
        return blacklist

    @commands.Cog.listener()
    async def on_message(self, msg):
        status = await self.get_status(msg.guild.id)
        if status == 'enabled':
            if not msg.author.guild_permissions.manage_messages: #If message author doesn't have manage_messages permission
                if str(msg.guild.id) in cache:
                    blacklist = cache[str(msg.guild.id)]
                else:
                    blacklist = await self.get_blacklist(msg.guild.id)

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
