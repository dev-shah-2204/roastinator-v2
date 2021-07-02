import discord 
import hex_colors 
import random

from discord.ext import commands
from io import BytesIO
from PIL import Image

class Bonk(commands.Cog):
    def __init__(self, client):
        self.client = client 

    @commands.command(name='bonk', help='Bonk the horny out of them')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def bonk(self, ctx, user:discord.Member=None):
        if user == None:
            user = ctx.author 

        image = Image.open('./images/bonk.jpg')
        avatar = user.avatar_url_as(size=64) #64x64 pixels
        data = BytesIO(await avatar.read())

        bonkee = Image.open(data)
        bonkee = bonkee.resize((80,53))

        image.paste(bonkee, (200,65)) #200,65 are the coordinates
        image.save('./images/bonked.jpg')

        await ctx.send(f"{ctx.author.mention} bonked {user.mention}", file=discord.File('./images/bonked.jpg'))


def setup(client):
    client.add_cog(Bonk(client))
    print('Bonk')