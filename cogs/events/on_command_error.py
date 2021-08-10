import discord
import random

import hex_colors
from discord.ext import commands


class ErrorHandling(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            em = discord.Embed(title='Error', color=hex_colors.m_red)
            em.add_field(name="Command incomplete", value=":x: | The command is incomplete")

            await ctx.send(embed=em)
            ctx.command.reset_cooldown(ctx)
            return

        if isinstance(error, commands.MissingPermissions):
            em = discord.Embed(title='Error', color=hex_colors.m_red)

            #This part is copy-pasted from a different source (I don't remember where.)
            missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]

            if len(missing) > 2:
                permission = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
            else:
                permission = ' and '.join(missing)

            em.add_field(name="Missing Permissions", value=f":x: | You need the {permission} permission to do that")
            await ctx.send(embed=em)
            return

        if isinstance(error, commands.MemberNotFound):
            em = discord.Embed(title='Error', color=hex_colors.m_red)
            em.add_field(name="Member not found", value=f":x: | I couldn't find anyone with that name in this server")

            await ctx.send(embed=em)
            ctx.command.reset_cooldown(ctx)
            return

        if isinstance(error, commands.BotMissingPermissions):
            mp = error.missing_perms[0]
            mp = mp.title()
            mp = mp.replace('_', ' ')

            em = discord.Embed(title='Error', color=hex_colors.m_red)
            em.add_field(name="I don't have the permission", value=f":x: | That command should have worked but I don't have the {mp} permission.")

            try:
                await ctx.send(embed=em)
                return
            except:
                await ctx.send(f"I don't have the {mp} permission. F") #In case the bot doesn't have embed links permission
            return


        if isinstance(error, commands.CommandOnCooldown):
            mode = "second(s)"
            if error.retry_after > 120:
                error.retry_after = error.retry_after//60
                mode = "minute(s)"

            if error.retry_after > 3600:
                error.retry_after = error.retry_after//3600
                mode = "hour(s)"

            em = discord.Embed(title="Error", color=hex_colors.m_red)
            em.add_field(name="Command on Cooldown", value=f":x: | The `{ctx.command}` command is on a cooldown, try again in **{error.retry_after:,.1f} {mode}**")
            await ctx.send(embed=em)
            return

        if isinstance(error, commands.BadArgument):
            em = discord.Embed(title = "Error", color=hex_colors.m_red)
            em.add_field(name="Invalid arguments", value = ":x: I think you used the command wrong. For more info, try running: ```-help {}```".format(ctx.command))
            await ctx.send(embed = em)
            ctx.command.reset_cooldown(ctx)
            return

        if isinstance(error, commands.CommandNotFound):
            return

        if isinstance(error, discord.Forbidden):
            em = discord.Embed(title = 'Error', color = hex_colors.m_red)
            em.add_field(name = 'Missing Permissions', value = ":x: Error code 403 Forbidden was raised. I don't have the permissons to do so.")

        else:
            await ctx.send("An error occured that I wasn't able to handle myself. This has been conveyed to my developer.")
            if ctx.author.id == 416979084099321866:
                print(error)
                return

            channel = self.client.get_channel(857878860251136020) #Enter your channel ID here
            em = discord.Embed(title = 'Error', color = hex_colors.m_red)

            em.add_field(name = 'Command', value = ctx.command, inline = False)
            em.add_field(name = 'Error:', value = f"```{error}```", inline = False)
            em.add_field(name = 'Server:', value = f"{ctx.guild} ({ctx.guild.id})", inline = False)
            em.add_field(name = 'User:', value = f"{ctx.author} ({ctx.author.id})", inline = False)
            em.add_field(name = 'Message:', value = ctx.message.content)

            await channel.send(embed = em)
        

def setup(client):
    client.add_cog(ErrorHandling(client))
    print("ErrorHandling")
