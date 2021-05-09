import discord, random

from discord.ext import commands
from discord.ext.commands import CommandOnCooldown, BucketType
import hex_colors

colors = hex_colors.colors

class Kick(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name = 'kick', help = 'Kick a member from the server', usage = '<member> [reason]')
    @commands.has_permissions(kick_members = True)
    @commands.bot_has_permissions(kick_members = True)
    async def kick(self, ctx, member:discord.Member, *, reason = None): #Default reason is "No reason provided"
        if reason == None:
            await ctx.send("You need to provide a reason")

        if member == self.client.user: #If  the 'member' is the bot
            await ctx.send("I don't know what the procedure is here, but I cannot leave like this. You'll have to remove me from the server manually. If I caused any problem, DM it to me, with details so my developer can fix me.")
            return

        if member == ctx.author: #If the 'member' is the person who invoked the command
            await ctx.send("Why do you wanna kick your self?")
            return

        #Checking if the other person has a higher role
        if member.top_role.position >= ctx.author.top_role.position:
            await ctx.send(f"{member.mention} has a higher role than you/same role as you. You cannot kick them")
            return

        try:
            await member.kick(reason = reason)
        except:
            await ctx.send(f"{member} has a higher role than me, I can't kick them")
            return


        em = discord.Embed(color = random.choice(colors))
        em.set_author(name = f"{ctx.author} kicked {member}", icon_url = ctx.author.avatar_url)
        em.set_thumbnail(url = member.avatar_url)
        em.add_field(name = 'Reason:', value = reason)

        await ctx.send(embed = em)


def setup(client):
    client.add_cog(Kick(client))
    print('Kick')
