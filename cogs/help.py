import discord

from utils import colors
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    @commands.command(name='help')
    async def help_command(self, ctx, cmd: str = None):
        if cmd is None:
            em = discord.Embed(
                title="Help is here",
                color=colors.l_green
            )
            em.add_field(
                name="Categories",
                value="Fun\nGames\nModeration\nUtility"
            )
            em.set_footer(text="Use 'help <category>' for more info")
            #em.set_image(url="https://share.creavite.co/0WJHeMtAYaVfFLQC.gif")  I don't really like the gif
            await ctx.reply(embed=em, mention_author=False)

        else:
            aliases = {}
            fun = []
            games = []
            mod = []
            util = []


            for command in self.bot.commands:
                aliases[command.name] = []

                if command.cog:
                    if command.cog.qualified_name == 'Fun':
                        fun.append(command.name)
                    elif command.cog.qualified_name == 'Games':
                        games.append(command.name)
                    elif command.cog.qualified_name == 'Moderation':
                        mod.append(command.name)
                    elif command.cog.qualified_name == 'Utility':
                        util.append(command.name)

                for alias in command.aliases:
                    aliases[command.name].append(alias)

            if cmd.lower() == 'fun':
                desc = ""
                for com in fun:
                    desc += f"`{com}`\n"

                em = discord.Embed(
                    title="Fun commands:",
                    description=desc,
                    color=colors.l_green
                )
                await ctx.reply(embed=em, mention_author=False)

            elif cmd.lower() == 'games':
                desc = ""
                for com in games:
                    desc += f"`{com}`\n"

                em = discord.Embed(
                    title="Games commands:",
                    description=desc,
                    color=colors.l_green
                )
                await ctx.reply(embed=em, mention_author=False)

            elif cmd.lower() == 'moderation' or cmd.lower() == 'mod':
                desc = ""
                for com in mod:
                    desc += f"`{com}`\n"

                em = discord.Embed(
                    title="Moderation commands:",
                    description=desc,
                    color=colors.l_green
                )
                await ctx.reply(embed=em, mention_author=False)

            elif cmd.lower() == 'utility' or cmd.lower() == 'util':
                desc = ""
                for com in util:
                    desc += f"`{com}`\n"

                em = discord.Embed(
                    title="Utility commands:",
                    description=desc,
                    color=colors.l_green
                )
                await ctx.reply(embed=em, mention_author=False)

            else:
                command = discord.utils.get(self.bot.commands, name=cmd.lower())

                if command is None:  # Gotta check if they entered an alias that they're familiar with
                    for com in aliases:
                        for als in aliases[com]:
                            if als == cmd.lower():
                                command = discord.utils.get(self.bot.commands, name=com)
                                break

                    if command is None:  # If still none after checking for aliases
                        await ctx.reply("That command does not exist", mention_author=False)
                        return

                _aliases = ", ".join([*command.aliases])
                if _aliases == '':
                    _aliases = "This command has no aliases"

                _help = command.help
                if _help is None:
                    _help = "No information"

                args = []
                for key, value in command.params.items():
                    if key not in ("self", "ctx"):
                        if "None" in str(value) or "No reason provided" in str(value):  # If that param is optional
                            args.append(f"[{key}]")
                        else:
                            args.append(f"<{key}>")

                args = " ".join(args)

                em = discord.Embed(
                    title=command.name.capitalize(),
                    description=_help,
                    color=colors.l_green
                )
                em.add_field(
                    name="Usage:",
                    value=f"```{command.name} {args}```",
                    inline=False
                )
                em.add_field(
                    name="Aliases",
                    value=_aliases
                )
                await ctx.reply(embed=em, mention_author=False)


def setup(bot):
    bot.add_cog(Help(bot))
    print("Help cog loaded")
