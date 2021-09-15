import discord 

from discord.ext import commands
from hex_colors import m_red as red


class Reply(commands.Cog):
    def __init__(self, client):
        self.client = client 
    
    @commands.command(name='mreply', help="This is a developer command")
    async def m_reply(self, ctx, user_id:int, *, reply_message):
        user = self.client.get_user(user_id)
        if user is None:
            await ctx.send("Couldn't find a user with that ID")
            return 
        
        em = discord.Embed(description=reply_message, color=red)
        em.set_author(icon_url=ctx.author.avatar_url, name=f"Message from {ctx.author} (My developer)")
        
        try:
            await user.send(embed=em)
            await ctx.send(f"Sent your reply to {user}")
        except discord.Forbidden: # If user doesn't allow messages from server members, we'll have to message them in a different way.
            await ctx.send(f"{user} has closed their DMs. The reply will be sent to them when they send a message in any server") 
            
            # def check(message: discord.Message) -> bool:
            #     return message.author == user
            #
            # message = await self.client.wait_for('message', check=check)
            #
            # try:
            #     await message.channel.send(f"<@!{user.id}>, your modmail has been replied to. Since your DMs are closed, we had to send it this way.")
            #     await message.channel.send(embed=em)
            #
            # except discord.Forbidden:
            #     await ctx.send(f"I tried replying to {user} in a server but I didn't have permission to send messages/embed links in that channel. Add them yourself and convey the message.")
            #     return


def setup(client):
    client.add_cog(Reply(client))
    print('Reply')