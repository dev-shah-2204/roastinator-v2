import discord
import os

from aiohttp import ClientSession 
from discord.ext import commands
from asyncio import sleep

class DadJoke(commands.Cog):
    def __init__(self, client):
        self.client = client 

    @commands.command(name='dadjoke', aliases=['dad'], help='Sends a dad joke.')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def dad_joke(self, ctx):
        url = "https://dad-jokes.p.rapidapi.com/random/joke"

        keys = [
        os.environ.get('dad_key_1'),
        os.environ.get('dad_key_2'),
        os.environ.get('dad_key_3'),
        os.environ.get('dad_key_4'),
        os.environ.get('dad_key_5'),
        os.environ.get('dad_key_6')
    ] #Each of these keys can be called 50 times a day. You can find another API or get more keys

        for key in keys:
            try:
                headers = {
                    'x-rapidapi-key': key,
                    'x-rapidapi-host': "dad-jokes.p.rapidapi.com"
                    }

                async with ClientSession() as session:
                    async with session.get(url, headers=headers) as response:
                        result = await response.json()
                        result = result["body"][0]

                        await ctx.send(f"**{result['setup']}**\n\n*{result['punchline']}*")
                        break 
            except:
                keys.remove(key)
                #Heroku will add it again after 12 hours when it clears cache or something.
                #If your hosting service doesn't do that, just write 'pass' instead of 'keys.remove(key)'


def setup(client):
    client.add_cog(DadJoke(client))
    print('DadJoke')