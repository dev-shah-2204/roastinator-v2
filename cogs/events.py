import discord
import json
import os
import asyncio

from pytz import timezone
from datetime import datetime
from discord.ext import commands
from discord.ext.commands import Cog
from utils import checks, colors
from db import *


people_on_cooldown = []
fixed_prefix = []  # If the bot was added when offline, prefix was probably not registered.

def check_ban(user):
    with open('./cache/banned.json', 'r') as f:
        banned_people = json.load(f)

    try:
        if user in banned_people['modban']:
            return True
    except KeyError:
        banned_people['modban'] = []

        with open('./cache/banned.json', 'w') as f:
            json.dump(banned_people, f)

    db.execute(f"SELECT user_id FROM ModBan WHERE user_id = '{user}'")

    if db.fetchone() is not None:
        banned_people['modban'].append(user)
        return True
    else:
        return False


class Events(Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot


    @Cog.listener()
    async def on_ready(self):
        print('---------')
        print('All cogs loaded')
        print(f"Date: {datetime.now(timezone('Asia/Kolkata')).strftime('%d - %m - %Y')}")
        print(f"Time: {datetime.now(timezone('Asia/Kolkata')).strftime('%H:%M')}")
        print(f"Servers: {len(self.bot.guilds)}")
        print(f"Users: {len(self.bot.users)}")

        await self.bot.wait_until_ready()
        await self.bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.listening,
                name='-help'
            )
        )


    @Cog.listener()
    async def on_message(self, msg):
        global people_on_cooldown

        if msg.author.bot:
            return

        # ModMail
        if isinstance(msg.channel, discord.DMChannel):
            if not msg.author.id in people_on_cooldown:
                check = check_ban(msg.author.id)
                if check is True:
                    await msg.channel.send("You have been banned from using ModMail. For further details, contact StatTrakDiamondSword#5493 or join the server discord.gg/GG647gySEy")
                    return


                    mod_channel = os.getenv('modmail_channel')
                    em = discord.Embed(
                        title="Mod-mail is here",
                        description=msg.content,
                        color=colors.l_red,
                        timestamp=datetime.now()
                    )
                    em.set_footer(text=f"Sent by {msg.author} | {msg.author.id}")
                    mod_channel.send(f"<@!{self.bot.owner.id}>,", embed=em)

                    people_on_cooldown.append(msg.author.id)
                    await asyncio.sleep(60)
                    people_on_cooldown.remove(msg.author.id)

            else:
                await msg.channel.send("You're on cooldown")
                return

        else:
            automod_status = checks.get_automod_status(msg.guild.id)
            if automod_status == 'enabled':
                print('enabled')
                blacklist = checks.get_blacklist(msg.guild.id)

                user = msg.guild.get_member(msg.author.id)
                if user is not None:
                    if not user.guild_permissions.manage_messages:

                        for word in blacklist:
                            if word.lower() in msg.content.lower():
                                await msg.delete()
                                try:
                                    await msg.author.send(f"Hey! That word is not allowed in this server")
                                except discord.Forbidden:
                                    pass
                                break

            # Prefix
            if msg.guild.id not in fixed_prefix:
                prefix = checks.get_server_prefix(msg)
                fixed_prefix.append(msg.guild.id)

            if msg.content == f"<@!{self.bot.user.id}>" or msg.content == f"<@{self.bot.user.id}>":
                prefix = checks.get_server_prefix(msg)
                em = discord.Embed(
                    title=f"My prefix for this server is `{prefix}`",
                    color=colors.l_green
                )
                await msg.channel.send(embed=em)



    @Cog.listener()
    async def on_guild_join(self, guild):
        db.execute(f"INSERT INTO Prefix(guild, prefix) VALUES ('{guild.id}', '-')")
        db.execute(f"INSERT INTO AutoMod(guild, _status) VALUES ('{guild.id}', 'disabled')")
        database.commit()

        em = discord.Embed(
            title="Hey there!",
            description=f"""
My name is Roastinator and I specialise in moderation and utility.
My prefix is `-`. If you wish to change it, use the prefix command.
You can also ping me instead of using the prefix. 
For example: {self.bot.user.mention} prefix `.` will change the prefix to `.`
""",
            color=colors.l_green
        )

        for channel in guild.text_channels:
            if guild.me.guild_permissions.send_messages and guild.me.guld_permissions.embed_links:
                await channel.send(embed=em)
                break


    @Cog.listener()
    async def on_guild_remove(self, guild):
        db.execute(f"DELETE FROM Prefix WHERE guild = '{guild.id}'")
        db.execute(f"DELETE FROM AutoMod WHERE guild = '{guild.id}'")

        try:
            db.execute(f"DROP TABLE am_{guild.id}")
        except:
            pass

        database.commit()



def setup(bot):
    bot.add_cog(Events(bot))
    print("Events cog loaded")