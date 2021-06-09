import discord
import json
import random
import hex_colors

from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
from aiohttp import ClientSession

class Meme(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name = 'meme', aliases = ['maymay'])
    @cooldown(1, 3, BucketType.user)
    async def meme(self, ctx):
        subreddit = 'memes' #change this to whatever subreddit you want
        url = f'https://meme-api.herokuapp.com/gimme/{subreddit}' #url of the api

        """
        There is reddit's official API too, but it's slower and also sometimes returns mp4(s) that the discord.Embed class can't process. This API is much better in my opinion. Also, both, this and reddit's API are free.
        """

        async with ClientSession() as session:
            async with session.get(url) as output:
                final = await output.json()
                image = final['image'] #the meme (a reddit post)
                title = final['title'] #the title of the reddit post

            footer_texts = [
                'Haha!',
                'Lol',
                'LMFAO',
                "That's funny",
                "I can't stop laughing."
            ]

            em = discord.Embed(title = title, color = random.choice(hex_colors.colors))
            em.set_image(url = image)
            em.set_footer(text = random.choice(footer_texts))

            await ctx.send(embed = em)


def setup(client):
    client.add_cog(Meme(client))
    print('Meme')
