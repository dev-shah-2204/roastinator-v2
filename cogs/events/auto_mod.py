import discord 

from discord.ext import commands 
from db import *
from cache import am

cache = am
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
            print(word)
            blacklist.append(word[0]) #word is a tuple

        cache[str(guild)] = []
        cache[str(guild)] = blacklist #Adding in cache
        print(blacklist)
        return blacklist


    @commands.Cog.listener()
    async def on_message(self, msg):
        status = await self.get_status(msg.guild.id)
        if status == 'enabled':
            member = msg.guild.get_member(msg.author.id)
            if member is not None:
                # if not member.guild_permissions.manage_messages: #If message author doesn't have manage_messages permission
                                       
                if str(msg.guild.id) in cache:
                    blacklist = cache[str(msg.guild.id)]
                    print(blacklist)

                else:
                    blacklist = await self.get_blacklist(msg.guild.id)
                    print(blacklist)
                    cache[str(msg.guild.id)] = blacklist
                    
                for words in blacklist:
                    print(words)
                    for word in words:
                        print(word)
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
