import discord
import hex_colors
import random
import requests

from discord.ext import commands


class Reddit(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='reddit', aliases=['subreddit', 'getredditpost'],
                      help='Gets a post from the subreddit provided')
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def get_reddit_post(self, ctx, *, subreddit):
        url = f'https://meme-api.herokuapp.com/gimme/{subreddit}'  # This api only sends posts with images or gifs.

        post = requests.get(url=url).json()
        # Check if the post is nsfw
        if 'nsfw' in post:  # Sometimes it raises KeyError
            if post['nsfw']:
                if not ctx.channel.is_nsfw():
                    await ctx.send("The post I got from that subreddit is marked NSFW. I cannot send it here")
                    return

        try:
            image = post['url']  # the image
            title = post['title']  # the title of the reddit post
            link = post['postLink']  # the link to the post

            em = discord.Embed(
                title=f"[{title}]({link})",
                color=random.choice(hex_colors.colors)
            )
            em.set_image(url=image)
            em.set_footer(
                text=f"👍 {post['ups']} | Author: u/{post['author']}")  # post['ups'] is the upvote count, post['author'] is the author

            await ctx.send(embed=em)
        except KeyError:
            await ctx.send(f"I couldn't find a subreddit called `{subreddit}`")


def setup(client):
    client.add_cog(Reddit(client))
    print('Reddit')
