import discord
import asyncio
import json

from discord.ext import commands
from discord.ext.commands import command, has_permissions, bot_has_permissions, group, cooldown, BucketType
from utils import colors
from utils import checks
from db import *


class Moderation(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    """
    I used triple quotes in some places where user input is being handled because people might enter " or ' where you don't expect them to.
    """

    @command(name='kick', help='Kick a member from your server')
    @has_permissions(kick_members=True)
    @bot_has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member, *, reason='No reason provided'):
        if user == self.bot.user:
            await ctx.reply("Should I leave? I don't understand. If I caused any problem, DM it to me so my developer can fix me", mention_author=False)
            return

        if user == ctx.author:
            await ctx.reply('Why do you want to kick yourself?', mention_author=False)
            return

        if user.top_role.position > ctx.author.top_role.position:
            await ctx.reply(f"{user.mention} has a higher role than you, you can't kick them", mention_author=False)
            return

        if user.top_role.position > ctx.guild.me.top_role.position:
            await ctx.reply(f"{user.mention} has a higher role than me, I can't kick them", mention_author=False)
            return

        if len(reason) > 256:
            await ctx.reply('The reason needs be shorter than 256 characters', mention_author=False)
            return

        em = discord.Embed(
            descrition=f"""**Reason**: {reason}""",
            color=colors.l_red)
        em.set_author(name=f'{ctx.author} kicked {user} from the server', icon_url=ctx.author.avatar_url)
        em.set_thumbnail(url=user.avatar_url)

        await user.kick(reason=f"""Kicked by {ctx.author}. Reason: {reason}""")
        await ctx.reply(embed=em, mention_author=False)


    @command(name='ban', help="Ban a member from your server")
    @has_permissions(ban_members=True)
    @bot_has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member, *, reason="No reason provided"):
        if user == self.bot.user:
            await ctx.reply("Should I leave? I don't understand. If I caused any problem, DM it to me so my developer can fix me", mention_author=False)
            return

        if user == ctx.author:
            await ctx.reply("Why do you want to ban yourself?", mention_author=False)
            return

        if user.top_role.position > ctx.author.top_role.position:
            await ctx.reply(f"{user.mention} has a higher role than you, you can't ban them", mention_author=False)
            return

        if user.top_role.position > ctx.guild.me.top_role.position:
            await ctx.reply(f"{user.mention} has a higher role than me, I can't ban them", mention_author=False)
            return

        if len(reason) > 256:
            await ctx.reply("The reason needs be shorter than 256 characters", mention_author=False)
            return

        em = discord.Embed(
            descrition=f"""**Reason**: {reason}""",
            color=colors.l_red)
        em.set_author(name=f"{ctx.author} banned {user} from the server", icon_url=ctx.author.avatar_url)
        em.set_thumbnail(url=user.avatar_url)

        await user.ban(reason=f"""Banned by {ctx.author}. Reason: {reason}""")
        await ctx.reply(embed=em, mention_author=False)


    @command(name='softban', help="Ban and unban a member from your server so all their messages get deleted")
    @has_permissions(kick_members=True)
    @bot_has_permissions(ban_members=True)
    async def soft_ban(self, ctx, user: discord.Member, *, reason="No reason provided"):
        if user == self.bot.user:
            await ctx.reply("Should I leave? I don't understand. If I caused any problem, DM it to me so my developer can fix me", mention_author=False)
            return

        if user == ctx.author:
            await ctx.reply("Why do you want to kick yourself?", mention_author=False)
            return

        if user.top_role.position > ctx.author.top_role.position:
            await ctx.reply(f"{user.mention} has a higher role than you, you can't kick them", mention_author=False)
            return

        if user.top_role.position > ctx.guild.me.top_role.position:
            await ctx.reply(f"{user.mention} has a higher role than me, I can't kick them", mention_author=False)
            return

        if len(reason) > 256:
            await ctx.reply("The reason needs be shorter than 256 characters", mention_author=False)
            return

        em = discord.Embed(
            descrition=f"""**Reason**: {reason}""",
            color=colors.l_red
        )
        em.set_author(name=f"{ctx.author} kicked {user} from the server", icon_url=ctx.author.avatar_url)
        em.set_thumbnail(url=user.avatar_url)

        await user.ban(reason=f"""Softbanned by {ctx.author}. Reason: {reason}""")
        await user.unban()
        await ctx.reply(embed=em, mention_author=False)


    @command(name='purge', aliases=['clear', 'delete', 'prune'], help="Delete messages in bulk")
    @has_permissions(manage_messages=True)
    @bot_has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int = 1):
        if amount <= 0:
            await ctx.reply("The number of messages needs to be greater than 0.", mention_author=False)
            return

        if amount > 150:
            await ctx.reply("Now, I could do that, but discord doesn't like it when I do that ¯\_(ツ)_/¯")
            return

        await ctx.channel.purge(limit=amount + 1)  # amount+1 because the command message is also included
        await ctx.send(f"**{ctx.author.name}** deleted {amount} messages", delete_after=5)  # reply wont work because the message got deleted


    @command(name='clean', help="Delete a lot bot messages")
    @has_permissions(manage_messages=True)
    @bot_has_permissions(manage_messages=True)
    async def clean(self, ctx):
        def is_bot(msg):
            return msg.author.bot == True

        await ctx.channel.purge(limit=100, check=is_bot)
        await ctx.reply(f"Deleted a lot of bot messages", mention_author=False)


    @command(name='nuke', help='Delete and re-create a channel')
    @has_permissions(manage_channels=True)
    @bot_has_permissions(administrator=True)
    async def nuke_channel(self, ctx, channel: discord.TextChannel = None,):
        if channel is None:
            channel = ctx.channel

        await ctx.reply("Type `confirm` if you wish to proceed with nuking the channel. Type `cancel`  if you do not wish to proceed with the same.", mention_author=False)

        try:
            def msg_author_check(message: discord.Message) -> bool:
                return message.author == ctx.author

            message = await self.bot.wait_for('message', timeout=15, check=msg_author_check)

            if message.content.lower() == 'cancel':
                await ctx.reply("Okay, cancelled", mention_author=False)
                return
            elif message.content.lower() == 'confirm':
                new_channel = await channel.clone(reason=f"Original was nuked by {ctx.author}")
                await new_channel.edit(position=channel.position)
                try:
                    await channel.delete()

                    em = discord.Embed(
                        title="This channel got nuked!",
                        description="Who did this? Check the audit log",  # Only the mods should know ig
                        color=colors.l_red
                    )
                    await new_channel.send(embed=em)

                except discord.Forbidden or discord.HTTPException:
                    await ctx.reply("Couldn't delete that channel. Is that the community updates channel?", mention_author=False)
                    await new_channel.delete()  # Clone kinda useless if original is still there
            else:
                await ctx.send("Invalid input. Cancelled the nuking", mention_author=False)
                return

        except asyncio.TimeoutError:
            await ctx.reply("You ran out of time, run the command again", mention_author=False)
            return


    @command(name='lock', aliases=['lockchannel'], help="Lock a channel")
    @has_permissions(manage_channels=True)
    @bot_has_permissions(manage_channels=True)
    async def lock_channel(self, ctx, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.channel

        await ctx.reply("Locking the channel. There's a high chance that I will get locked out too and won't be able to send the confirmation", mention_author=False)
        await channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await channel.set_permissions(ctx.guild.default_role, add_reactions=False)

        await ctx.send("Oh! I didn't get muted. Locked the channel successfully")


    @command(name='unlock', aliases=['unlockchannel'], help="Unlock a channel")
    @has_permissions(manage_channels=True)
    @bot_has_permissions(manage_channels=True)
    async def unlock_channel(self, ctx, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.channel

        await channel.set_permissions(ctx.guild.default_role, send_messages=True)
        await channel.set_permissions(ctx.guild.default_role, add_reactions=True)
        await ctx.send("Unlocked the channel")


    @command(name='mute', aliases=['shut', 'stfu'], help="Mute a member in your server")
    @has_permissions(manage_roles=True)
    @bot_has_permissions(manage_channels=True)
    @bot_has_permissions(manage_channels=True)
    async def mute_person(self, ctx, user: discord.Member, *, reason="No reason provided"):
        role = discord.utils.get(ctx.guild.roles, name='Muted')
        permissions = discord.Permissions(send_messages=False)
        fix_perms = False

        if role is None:
            fix_perms = True
            await ctx.reply("Hold on, making the `Muted` role. Don't worry, this process won't take place everytime you run this command")
            await ctx.guild.create_role(name='Muted', permissions=permissions, reason='For mute command')
            role = discord.utils.get(ctx.guild.roles, name='Muted')  # It might have returned 'None' first

        if role in user.roles:
            await ctx.reply(f"{user.mention} is already muted")
            return

        if role.position > ctx.guild.me.top_role.position:
            await ctx.send(f"The 'Muted' role is above my highest role, I can't mute {user}")
            return

        await user.add_roles(role, reason=f"Muted by {ctx.author}")

        em = discord.Embed(
            desription=f"""**Reason**: {reason}""",
            color=colors.l_red
        )
        em.set_author(
            name=f"{ctx.author.name} muted {user.name}",
            icon_url=ctx.author.avatar_url
        )
        em.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=em)

        if fix_perms:
            for channel in ctx.guild.channels:
                overwrite = channel.overwrites_for(role)
                overwrite.send_messages = False

                await channel.set_permissions(role, overwrite=overwrite)


    @command(name='unmute', aliases=['unshut', 'unstfu'], help="Unmute a member in your server")
    @has_permissions(manage_roles=True)
    @bot_has_permissions(manage_roles=True)
    async def unmute_person(self, ctx, user: discord.Member, *, reason="No reason provided"):
        role = discord.utils.get(ctx.guild.roles, name='Muted')
        permissions = discord.Permissions(send_messages=False)
        fix_perms = False

        if role is None:
            fix_perms = True
            await ctx.reply("Hold on, making the `Muted` role. Don't worry, this process won't take place everytime you run this command")
            await ctx.guild.create_role(name='Muted', permissions=permissions, reason='For mute command')
            role = discord.utils.get(ctx.guild.roles, name='Muted')  # It might have returned 'None' first

        if role not in user.roles:
            await ctx.reply(f"{user} isn't even muted", mention_author=False)
        else:
            await user.remove_roles(role, reason=f"Unmuted by {ctx.author}")

            em = discord.Embed(
                description=f"""**Reason**: {reason}""",
                color=colors.l_green
            )
            em.set_author(
                name=f"{ctx.author} unmuted {user}",
                icon_url=ctx.author.avatar_url
            )
            em.set_thumbnail(url=user.avatar_url)
            await ctx.send(embed=em)

        if fix_perms:
            for channel in ctx.guild.channels:
                overwrite = channel.overwrites_for(role)
                overwrite.send_messages = False

                await channel.set_permissions(role, overwrite=overwrite)


    @command(name='tempmute', aliaes=['tempshut', 'tempstfu'], help="Temporarily mute a member in your server")
    @has_permissions(manage_roles=True)
    @bot_has_permissions(manage_roles=True)
    async def temp_mute(self, ctx, user: discord.Member, time: int, mode: str = 'm', *, reason="No reason provided"):
        valid_modes = ('s', 'm', 'h', 'd', 'seconds', 'minutes', 'hours', 'days', 'second', 'minute', 'hour', 'day')

        if mode not in valid_modes:
            await ctx.reply("The mode of time needs to be either `s` for seconds or `m` for minutes or `h` for hours or `d` for days", mention_author=False)
            return

        if time <= 0:
            await ctx.reply("The time needs to be greater than 0", mention_author=False)
            return

        await self.mute_person(ctx=ctx, user=user, reason=reason)
        await ctx.send(f"Muted for {time}{mode}")

        multiplier = 1
        if mode == 's' or mode == 'second' or mode == 'seconds':
            multiplier = 1
        elif mode == 'm' or mode == 'minute' or mode == 'minutes':
            multiplier = 60
        elif mode == 'h' or mode == 'hour' or mode == 'hours':
            multiplier = 60 * 60
        elif mode == 'd' or mode == 'day' or mode == 'days':
            multiplier = 60 * 60 * 24

        await asyncio.sleep(time * multiplier)
        await user.remove_roles(discord.utils.get_role('Muted'), reason=f"Temporary mute is over. Responsible moderator: {ctx.author}")


    @command(name='prefix', aliases=['setprefix', 'change_prefix'], help="Change the prefix for your server")
    @has_permissions(manage_guild=True)
    async def change_prefix(self, ctx, new_prefix):
        if len(new_prefix) > 5:
            await ctx.reply("Thre prefix cannot be longer than 5 characters", mention_author=False)
            return

        if "'" in new_prefix or '"' in new_prefix:
            await ctx.reply("""The prefix cannot contain `"` or '`'.""")
            return

        guild = str(ctx.guild.id)

        with open('./cache/prefix.json', 'r') as f:
            cache = json.load(f)

        if guild in cache:
            if cache[guild] == new_prefix:
                await ctx.reply("The new prefix cannot be the same as your old prefix", mention_author=False)
                return

        db.execute(f"UPDATE Prefix SET prefix = '{new_prefix}' WHERE guild = '{guild}'")
        database.commit()

        em = discord.Embed(
            title='Prefix changed',
            description=f"New prefix: `{new_prefix}`",
            color=colors.l_green
        )
        await ctx.send(embed=em)

        cache[guild] = new_prefix

        with open('./cache/prefix.json', 'w') as f:
            json.dump(cache, f)


    @group(name='automod', aliases=['am'], help="Configure Auto Moderation settings for the server", invoke_without_command=True)
    @has_permissions(manage_messages=True)
    @bot_has_permissions(manage_messages=True)
    async def automod(self, ctx):
        em = discord.Embed(
            title="Commands:",
            description="`enable` \n`disable` \n`blacklist` \n`remove` \n`show`"
        )
        em.set_footer(text="Use 'automod <command>' to use a command")
        await ctx.reply(embed=em, mention_author=False)


    @automod.command(name='enable')
    @cooldown(1, 20 * 60, BucketType.user)
    async def automod_enable(self, ctx):
        status = checks.get_automod_status(str(ctx.guild.id))
        em = discord.Embed(
            description="Enabled Auto Mod for your server",
            color=colors.l_red
        )

        if status == 'enabled':
            await ctx.reply(embed=em, mention_author=False)
        else:
            db.execute(f"UPDATE AutoMod SET _status = 'enabled' WHERE guild = '{ctx.guild.id}'")
            database.commit()

            with open("./cache/automod.json", 'r') as f:
                cache = json.load(f)
            cache[str(ctx.guild.id)]['status'] = 'enabled'

            with open("./cache/automod.json", 'w') as f:
                json.dump(cache, f)

            await ctx.reply(embed=em, mention_author=False)


    @automod.command(name='disable')
    @cooldown(1, 20 * 60, BucketType.user)
    async def automod_disable(self, ctx):
        em = discord.Embed(
            description="Disabled Auto Mod for your server",
            color=colors.l_red
        )
        status = checks.get_automod_status(str(ctx.guild.id))
        if status == 'disabled':
            await ctx.reply(embed=em, mention_author=False)

        else:
            db.execute(f"UPDATE AutoMod SET _status = 'disabled' WHERE guild = '{ctx.guild.id}'")
            database.commit()

            with open("./cache/automod.json", 'r') as f:
                cache = json.load(f)

            if str(ctx.guild.id) not in cache:
                cache[str(ctx.guild.id)] = {}
                cache[str(ctx.guild.id)]['status'] = 'disabled'
                cache[str(ctx.guild.id)]['blacklist'] = []
            else:
                cache[str(ctx.guild.id)]['status'] = 'disabled'

            with open("./cache/automod.json", 'w') as f:
                json.dump(cache, f)

            await ctx.reply(embed=em, mention_author=False)


    @automod.command(name='blacklist', aliases=['bl'])
    async def blacklist_word(self, ctx, *, word):
        if len(word) > 40:
            await ctx.reply("Word length cannot exceed 40 characters", mention_author=False)
            return

        if '"' in word or "'" in word:
            await ctx.reply(f"""The word cannot contain `"` or `'`.""", mention_author=False)

        guild = str(ctx.guild.id)
        status = checks.get_automod_status(guild)
        blacklist = checks.get_blacklist(guild)

        if len(blacklist) >= 50:
            await ctx.send("Your server has already reached the 50 word blacklist limit. Remove some blacklisted words in order to blacklist more words or contact StatTrakDiamondSword#5493")
            return

        db.execute(f"INSERT INTO am_{guild} (words) VALUES ('{word}')")
        database.commit()

        with open('./cache/automod.json', 'r') as f:
            cache = json.load(f)

        cache[guild]['blacklist'].append(word)

        with open('./cache/automod.json', 'w') as f:
            json.dump(cache, f)

        em = discord.Embed(
            description=f'||{word}|| has been blacklisted in this server',
            color=colors.l_red
        )
        await ctx.reply(embed=em, mention_author=False)


    @automod.command(name='remove', aliases=['rm', 'unblacklist'])
    async def un_blacklist_word(self, ctx, *, word):
        guild = str(ctx.guild.id)
        status = checks.get_automod_status(guild)
        blacklist = checks.get_blacklist(guild)
        print(blacklist)

        if word not in blacklist:
            em = discord.Embed(
                description="That word isn't blacklisted in this server",
                color=colors.l_red
            )
            await ctx.reply(embed=em, mention_author=False)
            return

        db.execute(f"DELETE FROM am_{guild} WHERE words = '{word}'")
        database.commit()

        with open('./cache/automod.json', 'r') as f:
            cache = json.load(f)

        try:
            cache[guild]['blacklist'].remove(word)
        except ValueError:
            pass

        with open('./cache/automod.json', 'w') as f:
            json.dump(cache, f)

        em = discord.Embed(
            description=f"Removed '{word}' from the blacklist",
            color=colors.l_red
        )
        await ctx.reply(embed=em, mention_author=False)


    @automod.command(name='show', aliases=['list'])
    async def show_blacklist(self, ctx):
        guild = str(ctx.guild.id)
        blacklist = checks.get_blacklist(guild)
        desc = ""

        for word in blacklist:
            desc += f"`{word[0]}`\n"

        if desc == "":
            em = discord.Embed(
                description="There are no blacklisted words in your server",
                color=colors.l_red
            )
            await ctx.send(embed=em)
        else:
            em = discord.Embed(
                title="Blacklisted words in your server",
                description=desc,
                color=colors.l_red
            )
            await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Moderation(bot))
    print("Moderation cog loaded")
