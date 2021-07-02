import discord
import hex_colors

from discord.ext import commands

class Kick(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='kick', help='Kick a member from the server')
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self, ctx, user:discord.Member, *, reason="No reason provided"):
        member = user
        if member == self.client.user: #If  the 'member' is the bot
            await ctx.send("I don't know what the procedure is here, but I cannot leave like this. You'll have to remove me from the server manually. If I caused any problem, DM it to me, with details so my developer can fix me.")
            return

        if member == ctx.author: #If the 'member' is the person who invoked the command
            await ctx.send("Why do you wanna kick your self?")
            return

        #Checking if the other person has a higher role
        if member.top_role.position >= ctx.author.top_role.position:
            await ctx.send(f"{member} has a higher role than you/same role as you. You cannot kick them")
            return
        
        #Checking if the other person has a higher role than the bot
        if member.top_role.position >= ctx.guild.me.top_role.position:
            await ctx.send(f"{member} has a higher/same role than/as me. I can't kick them")
            return

        #Embed to be sent in the channel
        em = discord.Embed(color=hex_colors.m_red)
        em.set_author(name=f"{ctx.author} kicked {member}", icon_url=ctx.author.avatar_url)
        em.set_thumbnail(url=member.avatar_url)
        em.add_field(name='Reason:', value=reason)

        #Embed to be sent to the member 
        m_em = discord.Embed(color=hex_colors.m_red)
        m_em.set_author(name=f"{ctx.author} kicked you from {ctx.guild.name}", icon_url=ctx.author.avatar_url)
        m_em.set_thumbnail(url=ctx.guild.icon_url)
        m_em.add_field(name="Reason", value=reason)

        try:
            await member.send(embed=m_em)
        except:
            pass

        await member.kick(reason=reason)
        await ctx.message.delete()
        await ctx.send(embed=em)


def setup(client):
    client.add_cog(Kick(client))
    print('Kick')
