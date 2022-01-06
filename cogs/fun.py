import discord 
import os 
import requests 
import random

from io import BytesIO
from PIL import Image
from discord.ext import commands 
from discord.ext.commands import command, cooldown, BucketType
from utils import colors


class Fun(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot 

    @command(name='roast', aliases=['insult'], help="Roast someone. lol")
    @cooldown(1, 3, BucketType.user)
    async def roast(self, ctx, user: discord.Member=None):
        if user is None:
            user = ctx.author 
            
        if user.bot:
            await ctx.send("I'm not gonna roast someone of my own species")
            return 
        
        url = 'https://insult.mattbas.org/api/en/insult.json'  #Visit https://insult.matlabs.org/api/ for examples/documentaion
        r = requests.get(url, params={'who': user.mention}).json()
        
        await ctx.send(user.mention + r['insult'])
        
    
    @command(name='meme', aliases=['mamymay'], help="Sends a post from r/memes")
    @cooldown(1, 5, BucketType.user)
    async def send_memes(self, ctx):
        subreddit = 'memes'  # Change this to any subreddit that you want (like dankmemes)
        url = f"https://meme-api.herokuapp.com/gimme/{subreddit}"
        
        r = requests.get(url).json()
        image = r['url']
        title = r['title']
        
        if len(title) > 256:
            title = "<The title was too long>"
        
        em = discord.Embed(
            title=title,
            color=random.choice(colors.colors)
        )
        em.set_image(url=image)
        em.set_footer(text=f"👍 {r['ups']} | Author: u/{r['author']}")
        
        await ctx.send(embed=em)
    
    
    @command(name='wholesome', help="Sends a post from r/wholesomememes")
    @cooldown(1, 5, BucketType.user)
    async def wholesome_memes(self, ctx):
        subreddit = 'wholesomememes'  # Change this to any subreddit that you want
        url = f"https://meme-api.herokuapp.com/gimme/{subreddit}"
        
        r = requests.get(url).json()
        image = r['url']
        title = r['title']
        
        if len(title) > 256:
            title = "<The title was too long>"
        
        em = discord.Embed(
            title=title,
            color=random.choice(colors.colors)
        )
        em.set_image(url=image)
        em.set_footer(text=f"👍 {r['ups']} | Author: u/{r['author']}")
        
        await ctx.send(embed=em)
        
    
    @command(name='cursed', aliases=['cursedimage'], help="Sends a post from r/cursed_images")
    @cooldown(1, 5, BucketType.user)
    async def cursed_image(self, ctx):
        if not ctx.channel.is_nsfw():
            await ctx.send("This command only works in NSFW channels")
            return 
        
        url = "https://meme-api.herokuapp.com/gimme/cursed_images"
        
        r = requests.get(url).json()
        image = r['url']
        title = r['title']
        
        if len(title) > 256:
            title = "<The title was too long>"
        
        em = discord.Embed(
            title=title,
            color=random.choice(colors.colors)
        )
        em.set_image(url=image)
        em.set_footer(text=f"👍 {r['ups']} | Author: u/{r['author']}")
        
        await ctx.send(embed=em)
    
    
    @command(name='dadjoke', aliases=['dad'], help="Sends a dadjoke")
    @cooldown(1, 5, BucketType.user)
    async def dad_joke(self, ctx):
        url = "https://dad-jokes.p.rapidapi.com/random/joke"
        
        #Forgive me for doing this but
        keys = [
            os.getenv('dad_key_1'),
            os.getenv('dad_key_2'),
            os.getenv('dad_key_3'),
            os.getenv('dad_key_4'),
            os.getenv('dad_key_5'),
            os.getenv('dad_key_6')    
        ]  # I only get 50 calls per key per day (for free) :sad_emoji: 
        
        for key in keys:
            try:
                headers={
                    'x-rapidapi-key': key,
                    'x-rapidapi-host': 'dad-jokes.p.rapidapi.com'
                }
                
                r = requests.get(url=url, headers=headers).json()
                
                setup = r['body'][0]['setup']
                punchline = r['body'][0]['punchline']
                
                await ctx.send(f"**{setup}**\n\n*{punchline}*")    
                break
            except:
                keys.remove(key)  # I host my bot on heroku and the bot restarts every 12 hours (with the original code) so the keys get back into the list.
        
    
    @command(name='bonk', help="Send em to horny jail!")
    @cooldown(1, 5, BucketType.user)
    async def bonk(self, ctx, user: discord.Member=None):
        if user is None:
            user = ctx.author
            
        image = Image.open('./images/bonk.jpg')
        avatar = user.avatar_url_as(size=64)
        data = BytesIO(await avatar.read())
        
        bonkee = Image.open(data)
        bonkee = bonkee.resize((80, 53))  # Stretched image for bonk effect
        
        image.paste(bonkee, (200, 65))  # I spent over 10 minutes to find the right spot
        image.save('./images/bonked.jpg')
        
        await ctx.send(f"{ctx.author.name} bonked {user.mention}", file=discord.File('./images/bonked.jpg'))


def setup(bot):
    bot.add_cog(Fun(bot))
    print("Fun cog loaded")
