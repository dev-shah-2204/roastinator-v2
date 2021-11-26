import discord
import hex_colors

from db import *
from discord.ext import commands
from cogs.events.modmail import banned_people


class ModMail(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    # The banned people will be unbanned when you restart the bot. You need to setup a database. I am unable to do so on heroku for some reason.
    @commands.command(name='banmodmail', aliases=['banmm'], help="This is a developer command")
    async def banmodmail(self, ctx, user:discord.User, *, reason):
        if ctx.author.id != self.client.owner_id:
            await ctx.send("You can't do that")
            return

        else:
            db.execute(f"INSERT INTO ModBan (user_id) VALUES ('{user.id}')")
            database.commit()
            await ctx.send(f"Won't take mod-mail from {user} now")
            banned_people.append(user.id)

            em = discord.Embed(title="Un-banned from ModMail",
                               description=f"**Reason**: {reason}",
                               color=hex_colors.m_red)
            em.set_footer(text="Action taken by StatTrakDiamondSword#5493")
            try:
                user.send(embed=em)
            except:
                await ctx.send("User has closed DMs")



    # You might want to unban them later too
    @commands.command(name='unbanmodmail', aliases=['unbanmm'], help="This is a developer command")
    async def unbanmodmail(self, ctx, user:discord.User, reason):
        if ctx.author.id != self.client.owner_id:
            await ctx.send("You can't do that")
            return

        else:
            db.execute(f"DELETE FROM ModBan WHERE user_id = '{user.id}'")
            database.commit()
            await ctx.send(f"Unbanned {user} from the mod-mail blacklist")
            banned_people.remove(user.id)

            em = discord.Embed(title="Banned from ModMail",
                               description=f"**Reason**: {reason}",
                               color=hex_colors.m_red)
            em.set_footer(text="Action taken by StatTrakDiamondSword#5493")
            try:
                user.send(embed=em)
            except:
                await ctx.send("User has closed DMs")


def setup(client):
    client.add_cog(ModMail(client))
    print('ModMail')
