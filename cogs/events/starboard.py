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
        db.execute(f"SELECT channel FROM Starboard WHERE guild = '{guild}'")
        channel = await get_data(db = db)
        return channel

    async def get_star_guild_state(self, guild):
        db.execute(f"SELECT status FROM Starboard WHERE guild = '{guild}'")
        state = await get_data(db = db)
        return state

    starcount = {}

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.emoji.name == '⭐':
            channel = await self.get_star_channel(payload.guild_id)
            if channel is None:
                return

            state = await self.get_star_guild_state(payload.guild.id)
            if state is 'enabled':
                msg_channel = await self.client.get_channel(payload.channel_id)
                msg = await msg_channel.fetch_message(payload.message_id)            
                user = await self.client.get_user(payload.user_id)

                if not payload.member.guild_permissions.manage_messages: #If the member doesn't have manage_messages permission
                    await msg_channel.send(f"{user.mention}, You need `Manage Messages` permission to star messages")
                    return 

                em = discord.Embed(
                    description = f"[Jump to message]({msg.jump_url})", #jump_url is the message link
                    color = hex_colors.l_yellow,
                    timestamp = msg.created_at 
                    )
                em.set_author(name = f"{user.name} starred a message", icon_url = user.avatar_url)

                if len(msg.attachments) > 0:
                    em.set_image(url = msg.attachments[0].url)

                em.add_field(name = f"{msg.author} said:", value = msg.content)
                
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