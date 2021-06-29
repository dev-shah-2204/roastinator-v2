import discord 
import mysql.connector
import hex_colors

from db import *
from discord.ext import commands 

db = database.cursor()

class StarboardEvent(commands.Cog):
    def __init__(self, client):
        self.client = client 

    async def get_star_channel(self, guild):
        db.execute(f"SELECT _channel FROM Starboard WHERE guild = '{guild}'")
        channel = await get_data(db = db)
        return channel

    async def get_star_guild_status(self, guild):
        db.execute(f"SELECT _status FROM Starboard WHERE guild = '{guild}'")
        status = await get_data(db = db)
        return status

    starcount = {}
    error = []

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.emoji.name == '⭐':
            channel = await self.get_star_channel(payload.guild_id)
            if channel is None:
                return
            channel = self.client.get_channel(int(channel))
            status = await self.get_star_guild_status(payload.guild_id)
            if status == 'enabled':
                msg_channel = self.client.get_channel(payload.channel_id)
                msg = await msg_channel.fetch_message(payload.message_id)            
                user = self.client.get_user(payload.user_id)

                if not payload.member.guild_permissions.manage_messages: #If the member doesn't have manage_messages permission
                    if user.id not in self.error:
                        await msg_channel.send(f"{user.mention}, You need `Manage Messages` permission to star messages")
                        self.error.append(user.id) #So that they can't make the bot spam
                        return 
                    return

                em = discord.Embed(
                    color = hex_colors.l_yellow,
                    timestamp = msg.created_at 
                    )
                em.set_author(name = f"{user.name} starred a message", icon_url = user.avatar_url)
                
                if len(msg.attachments) > 0:
                    em.set_image(url = msg.attachments[0].url)

                desc = msg.content
                if msg.content == '':
                    desc = 'This message had an embed or an image'
                em.add_field(name = f"{msg.author} said:", value = f"{desc}\n\n[Jump to message]({msg.jump_url})")
                
                starcount = self.starcount

                #Only the first reaction should star the message
                if str(payload.message_id) in starcount:
                    starcount[str(payload.message_id)] += 1

                if not str(payload.message_id) in starcount:
                    starcount[str(payload.message_id)] = 1

                if starcount[str(payload.message_id)] <= 1:
                    await channel.send(embed = em)

                if starcount[str(payload.message_id)] > 1:
                    return

        
def setup(client):
    client.add_cog(StarboardEvent(client))
    print('StarboardEvent')