import discord

from discord.ext import commands


class Invite(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='invite', aliases=['addbot'])
    async def invite(self, ctx):
        em = discord.Embed(
            title="Thank you for inviting me",
            description="Click [here](https://discord.com/api/oauth2/authorize?client_id=822795444089782293&permissions=2013654102&scope=bot) to add me to your server\nClick [here](discord.gg/GG647gySEy) to join the support server."
        )
        em.set_thumbnail(url=self.client.user.avatar_url)
        em.set_footer(text='Bot created by StatTrakDiamondSword#9696 (Tag maybe outdated)')

        await ctx.send(embed=em)


def setup(client):
    client.add_cog(Invite(client))
    print('Invite')
