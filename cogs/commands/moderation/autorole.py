import discord 
import hex_colors

from db import *
from discord.ext import commands 

db = database.cursor()

class AutoRole(commands.Cog):
    def __init__(self, client):
        self.client = client 

    @commands.group(name = 'autorole', aliases = ['ar'], help = "Configure the auto-role setting", invoke_without_command = True)
    async def auto_role(self, ctx):
        em = discord.Embed(
            title = "Auto-Role",
            description = """
`set`
`enable`
`disable`""",         
            color = hex_colors.m_red
        )
        await ctx.send(embed = em)

    @auto_role.command(name = 'set', help = 'Set the role to be given to new members')
    @commands.has_permissions(manage_roles = True)
    @commands.bot_has_permissions(manage_roles = True)
    async def _set(self, ctx, role:discord.Role):
        try:
            db.execute(f"INSERT INTO AutoRole(guild, _role, _status) VALUES ('{ctx.guild.id}','{role.id}','enabled')")
        except:
            db.execute(f"UPDATE AutoRole SET _role = '{role.id}' WHERE guild = '{ctx.guild.id}'")
        database.commit()

        em = discord.Embed(
            title = 'Set auto-role',
            description = role.mention,
            color = hex_colors.m_red)
        em.set_footer(text = f"Action taken by {ctx.author}", icon_url = ctx.author.avatar_url)
        await ctx.send(embed = em)
    
    @auto_role.command(name = 'disable', help = 'Disable auto-role in your server')
    @commands.has_permissions(manage_roles = True)
    @commands.bot_has_permissions(manage_roles = True)
    async def disable_autorole(self, ctx):
        try:
            db.execute(f"UPDATE AutoRole SET _status = 'disabled' WHERE guild = '{ctx.guild.id}'")
            database.commit()
        except:
            await ctx.send("You have to configure the auto-role setting first to do that")

    @auto_role.command(name = 'enable', help = 'Enable auto-role in your server')
    @commands.has_permissions(manage_roles = True)
    @commands.bot_has_permissions(manage_roles = True)
    async def enable_autorole(self, ctx):
        try:
            db.execute(f"UPDATE AutoRole SET _status = 'enable' WHERE guild = '{ctx.guild.id}'")
            database.commit()
        except:
            await ctx.send("You have to configure the auto-role setting first to do that")


def setup(client):
    client.add_cog(AutoRole(client))
    print('AutoRole')