"""
Having trouble figuring out cogs? Check the on_message.py file
"""
import discord, re, sys, os

from discord.ext import commands
from discord.ext.commands import cooldown, CommandOnCooldown, BucketType

class Python(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name = 'python', aliases = ['py'], help = 'Run a python code line in discord', usage = '<code>')
    @cooldown(1, 10, BucketType.user)
    async def python_code(self, ctx, *, code):
        if 'import' in code:
            await ctx.send("Hey hey! You cannot import libraries yet.")
            return

        if 'quit(' in code or 'exit(' in code or 'input(' in code or 'sys.' in code or 'os.' in code: #So that they cannot do anything to our computer or turn off the bot
            await ctx.send("Yeah really smart, but you're not the only one who's smart here")
            return

        while_loops = re.search(r'while[\s\w_\s]+==[\sTrue:False:]', code) #Checking for while loops
        for_loops = re.search(r'for[\s\w_\s]+in[\s\w_(,)\s]+:', code) #Checking for for loops (for for xD)

        if 'open(' in code or 'close(' in code: #We don't want people to access our files
            await ctx.send("You cannot open or close files")
            return

        if while_loops or for_loops or 'while True:' in code:
            await ctx.send("Come on you can't run loops here. If you really want to, you can try https://repl.it")
            return


        sys.stdout = open('cogs/commands/utility/code_run_by_users.txt', 'w')#Output will be written in this file instead of terminal
        exec(code)
        sys.stdout.close()#If we don't close, the file is active and the data isn't saved

        return_code = open('cogs/commands/utility/code_run_by_users.txt', 'r')
        return_code_string = return_code.read()
        return_code.close()

        await ctx.send(f"```\n{return_code_string}\n```")

def setup(client):
    client.add_cog(Python(client))
    print('Python')
