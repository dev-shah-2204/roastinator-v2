import discord

from .. import hex_colors
from discord.ext import commands
#from ..events import on_message #To access the people_on_cooldown list
from ..events.on_message import people_on_cooldown


owner_id = 416979084099321866 #Replace with your ID
butcher_id = 414992506665828364 #This is my friend's ID you don't need to copy

class DeveloperCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    #Since we made the mod-mail, there are going to be spammers. What do we do? We give them a permanent cooldown. But this cooldown will expire when the bot restarts, since we dd
    @commands.command(name = 'banmodmail', help = 'Ban people from mod-mail', usage = '<user id>')
    async def banmodmail(self, ctx, user:discord.User):
        if ctx.author.id != owner_id: 
            await ctx.send("You can't do that")
            return

        else:
            people_on_cooldown.append(user.id)
            await ctx.send(f"Won't take mod-mail from {user.name}#{user.discriminator} now")
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
            await ctx.send(f"Unbanned {user.name}#{user.discriminator} from the mod-mail blacklist")
            owner = self.client.get_user(owner_id) 
            await owner.send(f"{user.id} has been un-banned from mod-mail")
            return


    @commands.command(name = 'reload', help = 'Reloads a cog')
    async def reload_cog(self, ctx, cog):
        if ctx.author.id != owner_id:
            await ctx.send("That is a developer command, you can't use that")
            return

        self.client.unload_extension(f"cogs.{cog}")
        self.client.load_extension(f"cogs.{cog}")
        await ctx.send(f"Reloaded {cog} cog")


    #Turn off the bot without going to the terminal
    @commands.command(name = 'restart', help = 'Restart the bot', usage = '')
    async def shutdown(self, ctx):
        if ctx.author.id != owner_id:
            await ctx.send("That is a developer command, you can't use that")
            return

        await ctx.send("Good night")
        quit() #Heroku thinks that the application crashed and restarts it

    #Load a cog that might haven't loaded because of a syntax error
    @commands.command(name = 'load', help = 'Loads a cog', usage = '<cog>')
    async def load_cog(self, ctx, cog):
        if ctx.author.id != owner_id:
            await ctx.send("That is a developer command, you can't use that")
            return

        self.client.load_extension(f"cogs.{cog}")
        await ctx.send(f"Loaded {cog} cog")

    
    #Unload a cog that you want to temporarily disable
    @commands.command(name = 'unload', help = 'Unloads a cog', usage = '<cog>')
    async def unload_cog(self, ctx, cog):
        if ctx.author.id != owner_id:
            await ctx.send("That is a developer command, you can't use that")
            return 
        
        self.client.unload_extension(cog)
        await ctx.send(f"Unloaded {cog} cog")


    #Run a python code, but in the bot's terminal. How this is different from the `python` command? You can access files and data of the bot
    @commands.command(name = 'eval', help = "Run a python code line, but it's different")
    async def eval_command(self, ctx, *, code):
        if ctx.author.id != owner_id:
            await ctx.send("That is a developer command, you can't use that")
            return

        elif ctx.author.id == owner_id:
            await eval(code)

        elif ctx.author.id == butcher_id:
            await eval(code)



def setup(client):
    client.add_cog(DeveloperCommands(client))
    print('DeveloperCommands Command cog loaded')