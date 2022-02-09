import discord
import json

from utils import colors
from discord.ext import commands
from discord.ext.commands import command, is_owner
from db import *


class Developer(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot
        
    @command(name='reload')
    @is_owner()
    async def reload_cog(self, ctx, cog):
        try:
            self.bot.unload_extension(f"cogs.{cog}")
            self.bot.load_extension(f"cogs.{cog}")
            
            em = discord.Embed(
                title="Cog Reloaded",
                description=f"cogs/{cog}",
                color=colors.l_red
            )
            await ctx.reply(embed=em)
        except Exception as e:
            em = discord.Embed(
                title="Error!",
                description=f"```{e}```",
                color=colors.l_red
            )
            await ctx.reply(embed=em)
            
    @command(name='load')
    @is_owner()
    async def load_cog(self, ctx, cog):
        try:
            self.bot.load_extension(f"cogs.{cog}")
            
            em = discord.Embed(
                title="Cog Loaded",
                description=f"cogs/{cog}",
                color=colors.l_red
            )
            await ctx.reply(embed=em)
        except Exception as e:
            em = discord.Embed(
                title="Error!",
                description=f"```{e}```",
                color=colors.l_red
            )
            await ctx.reply(embed=em)
            
    @command(name='unload')
    @is_owner()
    async def unload_cog(self, ctx, cog):
        try:
            self.bot.unload_extension(f"cogs.{cog}")
            
            em = discord.Embed(
                title="Cog unloaded",
                description=f"cogs/{cog}",
                color=colors.l_red
            )
            await ctx.reply(embed=em)
        except Exception as e:
            em = discord.Embed(
                title="Error!",
                description=f"```{e}```",
                color=colors.l_red
            )
            await ctx.reply(embed=em)


    @command(name="ignore")
    @is_owner()
    async def ignore_people(self, ctx, user: str):
        db.execute(f"INSERT INTO command_blacklist (user_id) VALUES ('{user}')")
        database.commit()

        with open('./cache/banned.json', 'r') as f:
            cache = json.load(f)

        if cache == {}:
            cache['banned'] = []

        if user not in cache['banned']:
            cache['banned'].append(user)

        with open('./cache/banned.json', 'w') as f:
            json.dump(cache, f)

        await ctx.reply(f"Added {user} to the blacklist")


    @command(name="unignore")
    @is_owner()
    async def unignore_people(self, ctx, user: str):
        db.execute(f"DELETE FROM command_blacklist WHERE user_id = '{user}'")
        database.commit()

        with open('./cache/banned.json', 'r') as f:
            cache = json.load(f)

        if cache == {}:
            cache['banned'] = []

        if user in cache['banned']:
            cache['banned'].remove(user)

        with open('./cache/banned.json', 'w') as f:
            json.dump(cache, f)

        await ctx.reply(f"Removed {user} from the blacklist")
    
    
    @command(name='banmodmail')
    @is_owner()
    async def ban_modmail(self, ctx, user: discord.User, *, reason = "No reason provided"):
        db.execute(f"INSERT INTO ModBan (user_id) VALUES ('{user.id}')")
        database.commit()
        await ctx.send(f"Won't take mod-mail from {user} now")

        em = discord.Embed(title="Banned from ModMail",
                           description=f"**Reason**: {reason}",
                           color=colors.l_red)
        em.set_footer(text="Action taken by StatTrakDiamondSword#5493")
        try:
            await user.send(embed=em)
        except:
            await ctx.send("User has closed DMs")

        with open('./cache/banned.json', 'r') as f:
            cache = json.load(f)

        cache['modban'].append(user.id)
        with open('./cache/banned.json', 'w') as f:
            json.dump(cache, f)

    @command(name='unbanmodmail')
    @is_owner()
    async def unban_modmail(self, ctx, user: discord.User, *, reason = "No reason provided"):
        db.execute(f"DELETE FROM ModBan WHERE user_id = '{user.id}'")
        database.commit()
        await ctx.send(f"Will take mod-mail from {user} now")

        em = discord.Embed(title="Un-banned from ModMail",
                           description=f"**Reason**: {reason}",
                           color=colors.l_red)
        em.set_footer(text="Action taken by StatTrakDiamondSword#5493")
        try:
            await user.send(embed=em)
        except:
            await ctx.send("User has closed DMs")

        with open('./cache/banned.json', 'r') as f:
            cache = json.load(f)
        try:
            cache['modban'].remove(user.id)
        except ValueError:
            pass

        with open('./cache/banned.json', 'w') as f:
            json.dump(cache, f)


    @command(name='modreply')
    @is_owner()
    async def modmail_reply(self, ctx, user_id: int, *, msg):
        user = self.bot.get_user(user_id)
        if user is None:
            await ctx.send("User not in any server with the bot/User not found")
            return

        em = discord.Embed(
            description=msg,
            color=colors.l_red
        )
        em.set_author(
            name=f"Message from {ctx.author} (My developer)",
            icon_url=ctx.author.display_avatar.url
        )

        try:
            await user.send(embed=em)
            await ctx.send(f"Sent your reply to {user}")
        except discord.Forbidden:
            await ctx.send(f"{user} has closed DMs.")



def setup(bot):
    bot.add_cog(Developer(bot))
    print("Developer cog loaded")
