"""
Having trouble figuring out cogs? Check the on_message.py file
"""
import discord
import random
import datetime
import hex_colors

from discord.ext import commands
from discord.ext.commands import cooldown, BucketType, Cog

class UserInfo(Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name = 'userinfo', aliases = ['whois'], help = 'Shows the details of a member', usage = '[member]')
    @cooldown(1, 10, BucketType.user)
    async def whois(self, ctx, member:discord.Member = None):
        if member == None:
            member = ctx.author

        created = member.created_at.strftime("%d %B %Y at %I %p") #The member.created_at attribute is in datetime.datetime format
        id = member.id #id is a keyword in python but we can use it as a variable name too.
        joined = member.joined_at.strftime("%d %B %Y at %I %p")

        member_role_list = []
        for role in ctx.guild.roles: #In order to present the roles in a decorative way
            if role in member.roles and role.name != '@everyone': #Because it logs @everyone as @@everyone
                member_role_list.append(role.id)

        roles = "@everyone " #@everyone is a default role
        for member_role in member_role_list:
            roles += f"<@&{member_role}> "


        em = discord.Embed(title = f"Found information for {member}", color = random.choice(hex_colors.colors))
        em.set_thumbnail(url = member.avatar_url)
        em.add_field(name = "ID", value = id, inline = False)
        em.add_field(name = "Account Created on", value = created, inline = False)
        em.add_field(name = "Joined Server on", value = joined, inline = False)
        em.add_field(name = "Roles in this Server", value = roles, inline = False)
        em.set_footer(text = f"Requested by {ctx.author.nick}", icon_url = ctx.author.avatar_url)

        await ctx.send(embed = em)

def setup(client):
    client.add_cog(UserInfo(client))
    print('UserInfo')
