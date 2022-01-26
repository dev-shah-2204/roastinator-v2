import discord 

from discord.ext import commands
from utils import colors


class Basic(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot 
        
    @commands.command(name='ping', help="Shows the bot's ping/latency")
    async def ping(self, ctx):
        latency = round(self.bot.latency*1000)
        if 10 < latency < 30:
            color = colors.l_green
        elif 30 < latency < 150:
            color = colors.l_yellow
        else:
            color = colors.l_red
            
        em = discord.Embed(
            title='Pong!',
            description=f"`{latency}`ms",
            color=color
        )
        await ctx.reply(embed=em, mention_author=False)
        
    
    @commands.command(name='invite', help="Invite the bot to your server")
    async def invite(self, ctx):
        owner = self.bot.get_user(self.bot.owner_id)
        em = discord.Embed(
            title="Thanks for inviting me!",
            description=f"Click [here](https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=8&scope=bot) to add me to your server",
            color=colors.l_green
        )
        em.set_footer(
            text=f"Bot created by {owner}",
            icon_url=owner.display_avatar.url
        )
        await ctx.reply(embed=em)
        

def setup(bot):
    bot.add_cog(Basic(bot))
    print("Basic cog loaded")
