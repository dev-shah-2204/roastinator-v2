import discord

from db import *
from discord.ext import commands
from cogs.events.modmail import banned_people


class ModMail(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    # The banned people will be unbanned when you restart the bot. You need to setup a database. I am unable to do so on heroku for some reason.
    @commands.command(name='banmodmail', aliases=['banmm'], help='Ban people from mod-mail')
    async def banmodmail(self, ctx, user:discord.User):
        if ctx.author.id != self.client.owner_id:
            await ctx.send("You can't do that")
            return

        else:
            db.execute(f"INSERT INTO ModBan (user_id) VALUES ('{user.id}')")
            database.commit()
            await ctx.send(f"Won't take mod-mail from {user} now")
            banned_people.append(user.id)

    # You might want to unban them later too
    @commands.command(name='unbanmodmail', aliases=['unbanmm'], help="Un-ban people from mod-mail")
    async def unbanmodmail(self, ctx, user:discord.User):
        if ctx.author.id != self.client.owner_id:
            await ctx.send("You can't do that")
            return

        else:
            db.execute(f"DELETE FROM ModBan WHERE user_id = '{user.id}'")
            database.commit()
            await ctx.send(f"Unbanned {user} from the mod-mail blacklist")
            banned_people.remove(user.id)


def setup(client):
    client.add_cog(ModMail(client))
    print('ModMail')
