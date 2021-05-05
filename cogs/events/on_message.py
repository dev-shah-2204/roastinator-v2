import discord
import random
import time
import asyncio

from asyncio import sleep
from datetime import datetime
from discord.ext import commands, tasks
from discord.ext.commands import BucketType, CommandOnCooldown
from .. import hex_colors  # Had to copy the hex_colors file from the main directory


people_on_cooldown = []
class OnMessage(commands.Cog, name = 'OnMessage'):
    def __init__(self, client):
        self.client = client

    

    @commands.Cog.listener()
    async def on_message(self, msg):
        global people_on_cooldown

        if msg.author.bot:
            return

        #Mod-Mail (Message for developers) This feature is not ideal if you plan on getting your bot into thousands of servers. Your ModMail Channel might get filled with spam
        
        mod_channel_id = 824977441503313980 #Paste your desired channel ID here

        if msg.channel.id == mod_channel_id and msg.author.id != self.client.user.id: #We dont want anyone to able to send a message in the Mod-Mail channel
            await msg.delete()

        

        if isinstance(msg.channel, discord.DMChannel): #Checking if the message channel is a DM channel
            if len(msg.content) < 40: #Mod-Mail must be detailed, we don't want spam
                await msg.channel.send("Thank you for reaching out to the Mod-Mail system. It appears that your message is shorter than 40 characters. The message in Mod-Mail is supposed to be in detail so that the mods of the bot can understand your problem. \n\nDid you not mean to reach out to the Mod-Mail? Well, nevermind then.")

                return

            else:
                if not msg.author.id in people_on_cooldown:
                
                    ModMail = discord.Embed(title = 'Mod-Mail is here',
                                            description = msg.content,
                                            color = hex_colors.m_red, #m_red is a new color in the hex_colors file. Go check it out,
                                            timestamp = datetime.now()
                    )
                    ModMail.set_thumbnail(url = msg.author.avatar_url)
                    ModMail.set_footer(text = f"Sent by {msg.author}")

                    mod_channel = self.client.get_channel(mod_channel_id) #We defined the channel, but python doesn't know that that's a channel. It interprets it as a regular integer.
                    await mod_channel.send(embed = ModMail)
                    
                    await msg.channel.send("Your message has been send to the developer(s). If you wish to send a ModMail again, you'll have to send it after a minute")

                    #Putting people on cooldown
                    people_on_cooldown.append(msg.author.id)
                    await sleep(60)
                    people_on_cooldown.remove(msg.author.id)

                else:
                    await msg.channel.send("It appears that you're either on a cooldown or banned from mod-mail because you spammed (maybe)")


#Setup           
def setup(client):
    client.add_cog(OnMessage(client))
    print('OnMessage Event cog loaded')
