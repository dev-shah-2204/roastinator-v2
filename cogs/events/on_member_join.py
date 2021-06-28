import discord 

from db import *
from discord.ext import commands

db = database.cursor()

class MemberJoin(commands.Cog):
    def __init__(self, client):
        self.client = client 

    async def get_status(self, guild):
        db.execute(f"SELECT _status FROM autorole WHERE guild = '{guild}'")
        status = await get_data(db = db)
        return status 

    async def get_role(self, guild):
        db.execute(f"SELECT _role FROM autorole WHERE guild = '{guild}'")
        role = await get_data(db = db)
        return role 

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        role = await self.get_role(guild.id)

        if role is None: #Server hasn't setup auto role
            return

        status = await self.get_status(guild.id)
        if status == 'enabled':
            await member.add_roles(role)
            



def setup(client):
    client.add_cog(MemberJoin(client))
    print('MemberJoin')