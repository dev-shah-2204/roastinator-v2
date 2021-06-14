import discord
import hex_colors
import random

from discord.ext import commands
from aiohttp import ClientSession


class Reddit(commands.Cog):
    def __init__(self, client):
        self.client = client 

    @commands.command(name = 'reddit', aliases = ['subreddit','getredditpost'], help = 'Gets a post from the subreddit provided')
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def get_reddit_post(self, ctx, *, subreddit):
        url = f'https://meme-api.herokuapp.com/gimme/{subreddit}' #This api only sends posts with images or gifs.


        async with ClientSession() as session:
            async with session.get(url) as output:
                post = await output.json()
                
                #Check if the post is nsfw
                if 'nsfw' in post: #Sometimes it raises KeyError
                    if post['nsfw'] == True:
                        if not ctx.channel.is_nsfw():
                            await ctx.send("The post I got from that subreddit is marked NSFW. I cannot send it here")
                            return
               
                image = post['url'] #the image
                title = post['title'] #the title of the reddit post

                em = discord.Embed(title = title, color = random.choice(hex_colors.colors))
                em.set_image(url = post['url'])
                em.set_footer(text = f"👍 {post['ups']} | Author: u/{post['author']}") #post['ups'] is the upvotes, post['author'] is the author

                await ctx.send(embed = em)


def setup(client):
    client.add_cog(Reddit(client))
    print('Reddit')