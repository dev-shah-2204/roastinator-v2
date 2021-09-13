import discord

from db import *
from datetime import datetime
from hex_colors import *
from discord.ext import commands
from asyncio import sleep

people_on_cooldown = []
banned_people = []


class ModMail(commands.Cog):  # Everything in a cog needs to be in a class
    def __init__(self, client):
        self.client = client

    async def check_ban(self, user):
        if user in banned_people:
            return True

        db.execute(f"SELECT user_id FROM ModBan WHERE user_id = '{user}'")
        if db.fetchone() is not None:
            banned_people.append(user)
            return True
        else:
            return False

    @commands.Cog.listener()  # Decorator for events in a cog. It's commands.Cog.listener() instead of client.event
    async def on_message(self, msg):  # Every function in a class needs 'self' as its first parameter
        global people_on_cooldown

        if msg.author.bot:  # If the author of the message is a bot
            return

        if isinstance(msg.channel, discord.DMChannel):  # Checking if the message channel is a DM DM Channel
            check = await self.check_ban(msg.author.id)
            if check is True:
                await msg.channel.send("You have been banned from ModMail. For further details contact my developer. You can join the support server, the link can be found here: https://discord.ly/roastinator")
                return

            if msg.author.id not in people_on_cooldown:  # Checking if the person is on cooldown
                ModMail = discord.Embed(title='Mod-Mail is here',
                                        description=msg.content,
                                        color=m_red,  # hex_colors file for more details
                                        timestamp=datetime.now()
                                        )
                ModMail.set_thumbnail(url=msg.author.avatar_url)
                ModMail.set_footer(text=f"Sent by {msg.author} | {msg.author.id}")

                mod_channel_id = 824977441503313980  # Paste your desired channel ID here
                mod_channel = self.client.get_channel(mod_channel_id)  # We defined the channel, but python doesn't know that that's a channel. It interprets it as a regular integer.

                await mod_channel.send("<@!416979084099321866>,")
                await mod_channel.send(embed=ModMail)

                await msg.channel.send("Your message has been send to the developer(s). If you wish to send a ModMail again, you'll have to send it after a minute")

                # Putting people on cooldown
                people_on_cooldown.append(msg.author.id)
                await sleep(60)
                people_on_cooldown.remove(msg.author.id)
                return

            if msg.author.id in people_on_cooldown:
                await msg.channel.send("It appears that you're on a cooldown")
                return


# Every cog needs this function. It's telling the main file that this is a cog/extension. It doesn't work like regular python modules
def setup(client):
    client.add_cog(ModMail(client))
    print('ModMail')  # So that we know when the cog is loaded when the bot starts
