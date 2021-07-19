import discord 

from discord.ext import commands 

class IgnorePeople(commands.Cog):
    def __init__(self, client):
        self.client = client 
        
    people_list = []
    
    @commands.Cog.listener()
    async def on_message(self, msg):
        if str(msg.author.id) in self.people_list:
            return 
        
    @commands.command(name = 'ignore')
    async def ignore(self, ctx, user_id):
        if ctx.author.id != 416979084099321866:
            return 
        
        self.people_list.append(user_id)   
    
    
        
def setup(client):
    client.add_cog(IgnorePeople(client))
    print("Ignore People")