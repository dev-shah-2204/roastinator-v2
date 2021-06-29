import discord 

from db import *
from discord.ext import commands

db = database.cursor(buffered = True)

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

        role = guild.get_role(int(role))
        status = await self.get_status(guild.id)
        if status == 'enabled':
            try:
                await member.add_roles(role)
            except:
                try:
                    await member.guild.owner.send("You setup the auto-role but either I don't have permissions to Manage Roles or my role is too low. Put my role above the role that you want me to assign to the users.")
                except:
                    def check(message:discord.Message) -> bool:
                        return message.author == user and message.guild == member.guild

                    message = await self.client.wait_for('message', check = check)
                    await message.channel.send(f"<@!{user.id}>, you setup the auto-role but either I don't have permissions to Manage Roles or my role is too low. Put my role above the role that you want me to assign to the users. Since your DMs are closed, I had to reply this way")
            

def setup(client):
    client.add_cog(MemberJoin(client))
    print('MemberJoin')