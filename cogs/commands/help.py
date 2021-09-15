import discord
import random
import hex_colors

from typing import Optional
from discord.ext import commands
from discord.ext.commands import command


pfpG = 0x60FF60 #my bot's pfp color

def decorate(command):
    args = []

    for key, value in command.params.items():
        if key not in ("self", "ctx"):
            if "None" in str(value) or "No reason provided" in str(value):
                args.append(f"[{key}]")
            else:
                args.append(f"<{key}>")

    args = " ".join(args)

    return f"```{command} {args}```"



class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def cmd_help(self, ctx, command): #Makes the embed
        _aliases = ', '.join([*command.aliases])
        if _aliases == '':
            _aliases = "Command has no aliases"

        _help = command.help
        if _help is None:
            _help = 'No help text provided by developer'

        em = discord.Embed(title=str(command).capitalize(), description=command.help, color=pfpG)
        em.add_field(name='Usage:', value=decorate(command), inline=False)
        em.add_field(name='Aliases:', value=_aliases, inline=False)

        await ctx.send(embed=em)

    @command(name='help', help='Shows this message')
    async def help(self, ctx, cmd: Optional[str]):
        if cmd is None: #Sends the default help message

            em = discord.Embed(title='Help is here', color=pfpG)
            em.add_field(name='Categories:', value="""
BotStats
Moderation
Utility
Games
Fun
""")
            em.set_footer(text="Use -help <category> for mor info")

            await ctx.send(embed=em)
            return

        aliases = {}

        for com in self.client.commands: #To get the alias list, will come in handy below
            aliases[com.name] = []
            for alias in com.aliases:
                aliases[com.name].append(alias)

        if cmd.lower() == 'fun':
            em = discord.Embed(
                title="Fun Commands",
                description='`meme` , `dadjoke`\n`wholesome` , `cursed`\n`roast`\n`bonk`',
                color=pfpG
            )
            em.set_footer(text='Use -help <command> for more info')
            await ctx.send(embed=em)
            return

        if cmd.lower() == 'games':
            em = discord.Embed(
                title="Games Commands",
                description='`cointoss` , `rockpaperscissors`',
                color=pfpG
            )
            em.set_footer(text='Use -help <command> for more info')

            await ctx.send(embed=em)
            return

        if cmd.lower() == 'moderation' or cmd.lower() == 'mod':
            em = discord.Embed(
                title="Moderation Commands:",
                description='`clear` , `clean` , `nuke`\n`kick` , `ban` , `softban`\n`mute` , `tempmute` , `unmute`\n`lock` , `unlock`\n`automod` , `autorole`',
                color=pfpG)
            em.set_footer(text='Use -help <command> for more info')

            await ctx.send(embed=em)
            return

        if cmd.lower() == 'utility' or cmd.lower() == 'util':
            em = discord.Embed(
                title="Utility Commands:",
                description='`avatar` , `roleinfo` , `serverinfo` , `userinfo`\n`snipe` , `editsnipe`\n`urban` , `reddit`  , `python` , `csgo` , `csgodetail`\n`embed` , `stealemoji` , `enlargeemoji` , `prefix` , `starboard`',
                color=pfpG)
            em.set_footer(text='Use -help <command> for more info')

            await ctx.send(embed=em)
            return

        if cmd.lower() == 'botstats' or cmd.lower() == 'bot':
            em = discord.Embed(
                title="Bot Stats Commands:",
                description="`invite` , `ping`",
                color=pfpG)
            em.set_footer(text='Use -help <command> for more info')

            await ctx.send(embed=em)
            return


        else:
            command = discord.utils.get(self.client.commands, name=cmd.lower()) #Trying to get the command from the command list

            if command is None: #If it cant find the command, it returns None. So now we check if the 'cmd' is an alias
                key_list = list(aliases.keys())
                val_list = list(aliases.values())

                for lst in val_list: #The big list of smaller lists
                    for e in lst: #The content of those smaller lists
                        if e == cmd.lower(): #If content matches the input
                            index1 = val_list.index(lst)

                try:
                    cmd_name = key_list[index1]
                except:
                    await ctx.send("That command does not exist")
                    return

                command = discord.utils.get(self.client.commands, name=cmd_name)

            await self.cmd_help(ctx, command)




def setup(client):
    client.add_cog(Help(client))
    print("Help Command cog loaded")
