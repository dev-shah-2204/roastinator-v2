import discord
import random

from datetime import datetime
from hex_colors import *
from discord.ext import commands

people_on_cooldown = []

class onMessage(commands.Cog): #Everything in a cog needs to be in a class
    def __init__(self, client):
        self.client = client


    @commands.Cog.listener() #Decorater for events in a cog. It's commands.Cog.listener() instead of client.event
    async def on_message(self, msg):#Every function in a class needs 'self' as its first parameter
        global people_on_cooldown

        if msg.author.bot: #If the author of the message is a bot
            return

        if isinstance(msg.channel, discord.DMChannel): #Checking if the message channel is a DM DM Channel
            if len(msg.content) < 40:
                await msg.channel.send(
                "Thank you for reaching out to the Mod-Mail system. It appears that your message is shorter than 40 characters. The message in Mod-Mail is supposed to be detailed, so the mods of the bot can understand your problem.\n\nDid you not mean to reach out to the Mod-Mail? Well, nevermind then")
                return

            else:
                if not msg.author.id in people_on_cooldown: #Checking if the person is on cooldown
                    ModMail = discord.Embed(title = 'Mod-Mail is here',
                                            description = msg.content,
                                            color = m_red, #hex_colors file for more details
                                            timestamp = datetime.now()
                    )
                    ModMail.set_thumbnail(url = msg.author.avatar_url)
                    ModMail.set_footer(text = f"Sent by {msg.author}")

                    mod_channel_id = 824977441503313980 #Paste your desired channel ID here
                    mod_channel = self.client.get_channel(mod_channel_id) #We defined the channel, but python doesn't know that that's a channel. It interprets it as a regular integer.

                    await mod_channel.send("<@!416979084099321866>,")
                    await mod_channel.send(embed = ModMail)

                    await msg.channel.send("Your message has been send to the developer(s). If you wish to send a ModMail again, you'll have to send it after a minute")

                    #Putting people on cooldown
                    people_on_cooldown.append(msg.author.id)
                    await sleep(60)
                    people_on_cooldown.remove(msg.author.id)
                    return

                else:
                    await msg.channel.send("It appears that you're either on a cooldown or banned from mod-mail because you spammed (maybe)")
                    return

        # if msg.content == f"<@!{self.client.user.id}>" or msg.content == f"<@{self.client.user.id}>": #When the bot is mentioned
        #     db.execute(f"SELECT prefix FROM Prefix WHERE guild = '{str(msg.guild.id)}'")
        #     for row in db:
        #         prefix = str(row).strip("('',)") #It's a tuple in the database, with a comma after the prefix string.
        #
        #     em = discord.Embed(title = f"My prefix for this server is: `{prefix}`", color = random.choice(colors))
        #     await msg.channel.send(embed = em)
        """
        The database code isn't working on heroku, until I figure that out, this part is disabled.
        """


#Every cog needs this function. It's telling the main file that this is a cog/extension. It doesn't work like regular python modules
def setup(client):
    client.add_cog(onMessage(client))
    print('onMessage') #So that we know when the cog is loaded when the bot starts
