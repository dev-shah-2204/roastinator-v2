import discord
import inspect 

from discord.ext import commands

owner_id = 416979084099321866 #Paste your ID here

class Cogs(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='reload', help='Reloads a cog')
    async def reload_cog(self, ctx, cog):
        if ctx.author.id != owner_id:
            await ctx.send("That is a developer command, you can't use that")
            return
        try:
            self.client.unload_extension(f"cogs.{cog}")
            self.client.load_extension(f"cogs.{cog}")
        except commands.ExtensionNotLoaded:
            self.client.load_extension(f"cogs.{cog}")
        
        await ctx.send(f"Reloaded {cog} cog")

    @commands.command(name='load', help='Loads a cog', usage='<cog>')
    async def load_cog(self, ctx, cog):
        if ctx.author.id != owner_id:
            await ctx.send("That is a developer command, you can't use that")
            return

        self.client.load_extension(f"cogs.{cog}")
        await ctx.send(f"Loaded {cog} cog")


    #Unload a cog that you want to temporarily disable
    @commands.command(name='unload', help='Unloads a cog', usage='<cog>')
    async def unload_cog(self, ctx, cog):
        if ctx.author.id != owner_id:
            await ctx.send("That is a developer command, you can't use that")
            return

        self.client.unload_extension(f"cogs.{cog}")
        await ctx.send(f"Unloaded {cog} cog")

    #This isn't a cog command but I didn't want to make a new file for it
    @commands.command(name='eval')
    async def eval_command(self, ctx, *, code):
        if ctx.author.id != owner_id:
            await ctx.send("That is a developer command, you can't use that")
            return 

        await ctx.send(await eval(str(code)))

def setup(client):
    client.add_cog(Cogs(client))
    print('Cogs')
