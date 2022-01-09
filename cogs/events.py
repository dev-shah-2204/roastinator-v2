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

def check_ban(user):
    with open('./cache/banned.json', 'r') as f:
        banned_people = json.load(f)

    if user in banned_people['modban']:
        return True

    db.execute(f"SELECT user_id FROM ModBan WHERE user_id = '{user}'")
    if db.fetchone() is not None:
        banned_people.append(user)
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

        # Auto Moderation (Not working properly)
        # automod_status = checks.get_automod_status(msg.guild.id)
        # if automod_status == 'enabled':
        #     print('enabled')
        #     blacklist = checks.get_blacklist(msg.guild.id)
        #
        #     user = msg.guild.get_member(msg.author.id)
        #     if user is not None:
        #         if not user.guild_permissions.manage_messages:
        #
        #             for word in blacklist:
        #                 if word.lower() in msg.content.lower():
        #                     await msg.delete()
        #                     try:
        #                         await msg.author.send(f"Hey! That word is not allowed in this server")
        #                     except discord.Forbidden:
        #                         pass
        #                     break

        # Prefix
        if msg.content == f"<@!{self.bot.user.id}>" or msg.content == f"<@{self.bot.user.id}>":
            prefix = checks.get_server_prefix(msg)

            em = discord.Embed(
                title=f"My prefix for this server is `{prefix}`",
                color=colors.l_green
            )
            await msg.channel.send(embed=em)


        #Command Blacklist
        # command_blacklist = checks.get_command_blacklist()
        #
        # if str(msg.author.id) in command_blacklist or msg.author.id in command_blacklist:
        #     print('in blacklist')
        #     return

    @Cog.listener()
    async def on_guild_join(self, guild):
        pass


    @Cog.listener()
    async def on_guild_remove(self, guild):
        pass





def setup(bot):
    bot.add_cog(Events(bot))
    print("Events cog loaded")