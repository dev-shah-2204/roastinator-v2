import discord
import hex_colors
from discord.ext import commands


class ErrorSender(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await ctx.send("An error occured that I wasn't able to handle myself. This has been conveyed to my developer.")
        await ctx.send(f"```{error}```")

        owner = self.client.get_user(416979084099321866) #Enter your ID here
        em = discord.Embed(title = 'Error', color = hex_colors.m_red)
        em.add_field(name = 'Command', value = ctx.command, inline = False)
        em.add_field(name = 'Error:', value = f"```{error}```", inline = False)
        em.add_field(name = 'Server:', value = f"{ctx.guild} ({ctx.guild.id})", inline = False)
        em.add_field(name = 'User:', value = f"{ctx.author} ({ctx.author.id})", inline = False)
        em.add_field(name = 'Message:', value = ctx.message.content)

        await owner.send(embed = em)
        
        
        #The embed is optional, I want to see it so that I can understand the problem and fix it. 

def setup(client):
    client.add_cog(ErrorSender(client))
    print("ErrorSender")
