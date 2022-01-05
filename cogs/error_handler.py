import discord
import os

from utils import colors
from discord.ext import commands


def reset_cooldown(ctx):
    """
    So you have to type reset_cooldown(ctx) instead of ctx.command.reset_cooldown(ctx)
    """
    ctx.command.reset_cooldown(ctx)


class ErrorHandler(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        em = discord.Embed(
            title="Error!",
            color=colors.l_red
        )

        if isinstance(error, commands.MissingRequiredArgument):
            em.add_field(
                name="Command incomplete",
                value=":x: | The command is incomplete"
            )
            await ctx.send(embed=em)
            reset_cooldown(ctx)

        elif isinstance(error, commands.MissingPermissions):
            perm = error.missing_perms[0]

            perm = perm.replace('_', ' ')
            perm = perm.replace('guild', 'server')
            perm = perm.title()

            em.add_field(
                name="Missing Permissions",
                value=f":x: | You need the {perm} permission to do that"
            )
            await ctx.send(embed=em)
            reset_cooldown(ctx)

        elif isinstance(error, commands.MemberNotFound):
            em.add_field(
                name="Member not found",
                value=":x: | I couldn't find anyone with that name in this server"
            )
            await ctx.send(embed=em)
            reset_cooldown(ctx)

        elif isinstance(error, commands.BotMissingPermissions):
            perm = error.missing_perms[0]

            perm = perm.replace('_', ' ')
            perm = perm.replace('guild', 'server')
            perm = perm.title()

            em.add_field(
                name="Missing Permissions",
                value=f":x: | I need the {perm} permission to do that"
            )
            await ctx.send(embed=em)
            reset_cooldown(ctx)

        elif isinstance(error, commands.CommandOnCooldown):
            mode = "second(s)"
            if error.retry_after > 120:
                error.retry_after = error.retry_after // 60
                mode = "minute(s)"

            if error.retry_after > 3600:
                error.retry_after = error.retry_after // 3600
                mode = "hour(s)"

            em.add_field(
                name="Command on Cooldown",
                value=f":x: | The `{ctx.command}` command is on a cooldown, try again in **{error.retry_after:,.1f} {mode}**")
            await ctx.send(embed=em)

        elif isinstance(error, commands.BadArgument):
            em.add_field(
                name="Invalid Usage",
                value=f":x: | I think you used that command wrong. For more info, try running: ```-help {ctx.command}```"
            )
            await ctx.send(embed=em)
            reset_cooldown(ctx)

        elif isinstance(error, commands.CommandNotFound):
            pass

        else:
            await ctx.send("An error occured that I wasn't able to handle myself. The details have been sent to my developer. For more information, contact StatTrakDiamondSword#5493")

            em.add_field(
                name="Command:",
                value=ctx.command,
                inline=False
            )
            em.add_field(
                name="Error:",
                value=f"```{type(error)}\n\n{error}```",
                inline=False
            )
            try:
                em.add_field(
                    name="Server:",
                    value=f"{ctx.guild.name} ({ctx.guild.id})",
                    inline=False
                )
                em.add_field(
                    name="Channel:",
                    value=f"{ctx.channel} ({ctx.channel.id})",
                    inline=False
                )
                em.add_field(
                    name="User:",
                    value=f"{ctx.author} ({ctx.author.id})"
                )
            except:
                em.add_field(
                    name="DM Channel",
                    value=f"{ctx.author} ({ctx.author.id})",
                    inline=False
                )
            em.add_field(
                name="Message:",
                value=ctx.message.content,
                inline=False
            )

            channel = self.bot.get_channel(int(os.getenv('error_channel')))
            if channel:
                await channel.send(embed=em)
            else:
                owner = self.bot.get_user(self.bot.owner_id)
                await owner.send(embed=em)


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
    print("ErrorHandler cog loaded")
