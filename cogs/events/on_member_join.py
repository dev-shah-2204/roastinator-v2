import discord 

from discord.ext import commands

class MemberJoin(commands.Cog):
    def __init__(self, client):
        self.client = client 

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id == 822816016614293595: #Auto role for the support server
            role = self.client.get_roles(858300138484924416)
            await member.add_role(role)

def setup(client):
    client.add_cog(MemberJoin(client))
    print('MemberJoin')