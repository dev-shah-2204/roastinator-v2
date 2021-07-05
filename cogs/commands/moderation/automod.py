import discord 
import hex_colors 

from cache import am as cache
from discord.ext import commands
from db import *



class AutoModCommands(commands.Cog):
    def __init__(self, client):
        self.client = client 


    @commands.group(name='automod', aliases=['am'], help="Configure AutoMod for the server", invoke_without_command=True)
    @commands.has_permissions(manage_messages = True)
    async def automod_cmds(self, ctx):
        em = discord.Embed(
            title="Available commands:",
            description="""
`enable`
`disable`
`blacklist`
`remove`
`show`
""")    
        em.set_footer(text="Use 'automod <command>' to use a command")

        if not ctx.guild.me.guild_permissions.manage_messages:
            await ctx.send("I need the `Manage Messages` permission for Auto Moderation")
            return 

        await ctx.send(embed=em)


    @automod_cmds.command(name='enable')
    async def automod_enable(self, ctx):
        try:
            db.execute(f"INSERT INTO AutoMod(guild, _status) VALUES('{ctx.guild.id}','enabled')")
            db.execute(f"CREATE TABLE IF NOT EXISTS am_{ctx.guild.id}(words VARCHAR(40) PRIMARY KEY)")
            databse.commit()
        except:
            db.execute(f"UPDATE AutoMod SET _status = 'enabled' WHERE guild = '{ctx.guild.id}'")
            database.commit()
        finally:
            #Add in cache
            if str(ctx.guild.id) not in cache:
                cache[str(ctx.guild.id)] = []
            await ctx.send("Enabled Auto Mod for your server")


    @automod_cmds.command(name='disable')
    async def automod_disable(self, ctx):
        db.execute(f"UPDATE AutoMod SET _status = 'disabled' WHERE guild = '{ctx.guild.id}'")
        database.commit()
        await ctx.send("Disabled Auto Mod for your server")


    async def get_status(self, guild):
        db.execute(f"SELECT _status FROM AutoMod WHERE guild = '{guild}'")
        status = db.fetchone()
        return status


    @automod_cmds.command(name='blacklist', aliases=['bl','ban'])
    async def automod_blacklist(self, ctx, *, word:str):
        if len(word) > 40:
            await ctx.send("Word length cannot exceed 40 characters")
            return 
        
        db.execute(f"CREATE TABLE IF NOT EXISTS am_{ctx.guild.id}(words VARCHAR(40) PRIMARY KEY)") #If they didn't use the enable command first
        db.execute(f"INSERT INTO am_{ctx.guild.id}(words) VALUES ('{word}')")
        database.commit()
        await ctx.send(f"||{word}|| is now blacklisted from the server")
        
        status = await self.get_status(ctx.guild.id)
        if status == 'disabled' or status == None:
            await self.automod_enable(ctx)

        #Cache
        cache[str(ctx.guild.id)].append(cache)


    @automod_cmds.command(name='remove', aliases=['rm','unban'])
    async def automod_remove(self, ctx, *, word):
        status = await self.get_status(ctx.guild.id)
        if status == 'disabled' or status == None:
            await ctx.send("You need to enable Auto Mod first by running this command:```automod enable```")
            return
        
        try:
            db.execute(f"SELECT * FROM am_{ctx.guild.id}")
            lst = db.fetchall()
            blacklist = []
            for _word in lst:
                blacklist.append(_word[0])

            if word not in blacklist:
                await ctx.send("That word isn't blacklisted")

            db.execute(f"DELETE FROM am_{ctx.guild.id} WHERE words = '{word}'")
            database.commit()
            await ctx.send(f'Un-blacklisted `{word}`')
        except:
            await ctx.send("That word isn't blacklisted")
        finally:
            cache[str(ctx.guild.id)].remove(word) #The word might not be in the cache, so I put it in 'finally'

    @automod_cmds.command(name='show', aliases=['list'])
    async def automod_show(self, ctx):
        status = await self.get_status(ctx.guild.id)

        if status == 'disabled' or status == None:
            await ctx.send("You need to enable Auto Mod first by running this command:```automod enable```")
            return
        
        db.execute(f"SELECT * FROM am_{ctx.guild.id}")
        lst = db.fetchall()

        desc = ''

        for word in lst:
            desc += f"`{word[0]}`\n" #word is a tuple
        if desc == None:
            desc = f"{ctx.guild.name} has no blacklisted words"

        em = discord.Embed(
            title=f'Blacklisted words in {ctx.guild.name}',
            description=desc,
            color=hex_colors.m_red
        )
        await ctx.send(embed=em)



def setup(client):
    client.add_cog(AutoModCommands(client))
    print('AutoModCommands')