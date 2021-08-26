import discord 

from db import *
from discord.ext import commands 


class IgnorePeople(commands.Cog):
    def __init__(self, client):
        self.client = client 
        
    cache = []
    cache_updated = False
    
    @commands.Cog.listener()
    async def on_message(self, msg):
        _id = str(msg.author.id)

        if not self.cache_updated:
            db.execute("SELECT * FROM command_blacklist")
            db.fetchall()
            for tup in db:
                print(f"ignore tuple: {tup}")
                self.cache.append(str(tup[0]))
            self.cache_updated = True
        
        if str(_id) in self.cache:
            return
        
        
    @commands.command(name='ignore')
    async def ignore_people(self, ctx, user_id):
        if ctx.author.id != 416979084099321866:
            return 
        
        db.execute(f"INSERT INTO command_blacklist (user_id) VALUES ('{user_id}')")    
        database.commit() 
        self.cache.append(str(user_id))
        await ctx.send(f"Added {user_id} to the blacklist")


    @commands.command(name='unignore')
    async def unignore_people(self, ctx, user_id):
        if ctx.author.id != 416979084099321866:
            return
        
        db.execute(f"DELETE FROM command_blacklist WHERE user_id = '{user_id}'")
        database.commit()
        self.cache.remove(str(user_id))
        await ctx.send(f"Removed {user_id} from the blacklist")
    
        
def setup(client):
    client.add_cog(IgnorePeople(client))
    print("Ignore People")