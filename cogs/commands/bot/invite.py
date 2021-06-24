import discord

from discord.ext import commands

class Invite(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name = 'invite', aliases = ['addbot'])
    async def invite(self, ctx):
        em = discord.Embed(
            title = "Thank you for inviting me",
            value = "Click [here](https://discord.com/api/oauth2/authorize?client_id=822795444089782293&permissions=1879436375&scope=bot)"
        )
        em.set_thumbnail(url = self.client.user.avatar_url)
        em.set_footer(text = 'Some of the required permissions might not be required, but they are for future updates')

        await ctx.send(embed = em)

def setup(client):
    client.add_cog(Invite(client))
    print('Invite')
