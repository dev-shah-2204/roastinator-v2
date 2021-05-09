import discord
import os

from discord.ext import commands
from cogs.events.on_message import people_on_cooldown #people_on_cooldown is a list, it gets reset every 12 hours on heroku. you need to setup a database to store the banned people's id

owner_id = 416979084099321866 #Replace with your ID
butcher_id = 414992506665828364 #This is my friend's ID you don't need to copy

class ModMail(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name = 'banmodmail', help = 'Ban people from mod-mail', usage = '<user id>')
    async def banmodmail(self, ctx, user:discord.User):
        if ctx.author.id != owner_id:
            await ctx.send("You can't do that")
            return

        else:
            people_on_cooldown.append(user.id)
            await ctx.send(f"Won't take mod-mail from {user} now")
            owner = self.client.get_user(owner_id)
            await owner.send(f"{user.id} has been banned from mod-mail")
            return

    #You might want to unban them later too
    @commands.command(name = 'unbanmodmail', help = "Un-ban people from mod-mail", usage = '<user id>')
    async def unbanmodmail(self, ctx, user:discord.User):
        if ctx.author.id != owner_id:
            await ctx.send("You can't do that")
            return

        else:
            people_on_cooldown.remove(user.id)
            await ctx.send(f"Unbanned {user} from the mod-mail blacklist")
            owner = self.client.get_user(owner_id)
            await owner.send(f"{user.id} has been un-banned from mod-mail")
            return

def setup(client):
    client.add_cog(ModMail(client))
    print('ModMail')
