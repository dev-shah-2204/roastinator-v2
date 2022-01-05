import discord
import requests
import shutil
import urbandict
import os
import asyncio
import pytz

from datetime import datetime 
from discord.ext import commands
from discord.ext.commands import command, cooldown, BucketType, has_permissions, bot_has_permissions
from utils import colors, checks


del_msg = {}
edit_msg = {}


class Utility(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    @command(name='avatar', aliases=['av'], help="Shows a user's avatar in full size")
    @cooldown(1, 5, BucketType.user)
    async def avatar(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author

        png = user.avatar_url_as(format='png')
        jpeg = user.avatar_url_as(format='jpeg')
        webp = user.avatar_url_as(format='webp')
        try:
            gif = user.avatar_url_as(format='gif')
        except:
            gif = None

        if gif:
            download_links = f"Download as [png]({png}) | [jpeg]({jpeg}) | [gif]({gif})"
        else:
            download_links = f"Download as [png]({png}) | [jpeg]({jpeg}) | [webp]({webp})"

        em = discord.Embed(
            title=f"{user.name}'s avatar",
            description=download_links,
            color=user.color
        )
        em.set_image(url=user.avatar_url)
        em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)

        await ctx.reply(embed=em, mention_author=False)


    @command(name='userinfo', aliases=['whois'], help="Shows the details of a server member")
    @cooldown(1, 5, BucketType.user)
    async def user_info(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author

        created = user.created_at.strftime("%d %B %Y at %I %p")  # user.created_at: datetime.datetime
        joined = user.joined_at.strftime("%d %B %Y at %I %p")

        member_role_list = []
        for role in ctx.guild.roles:
            if role in user.roles and role.name != '@everyone':
                member_role_list.append(role.id)

        roles = ""  # @everyone is a default role
        for member_role in member_role_list:
            roles += f"<@&{member_role}> "

        if roles is None:
            roles = "User has no roles in this server."

        em = discord.Embed(title=f"Found information for {user}", color=user.color)
        em.set_thumbnail(url=user.avatar_url)
        em.add_field(name="ID", value=f"`{user.id}`", inline=False)
        em.add_field(name="Account Created on", value=created, inline=False)
        em.add_field(name="Joined Server on",  value=joined,  inline=False)
        em.add_field(name="Roles in this Server",  value=roles, inline=False)
        em.set_footer(text=f"Requested by {ctx.author.nick}", icon_url=ctx.author.avatar_url)

        await ctx.reply(embed=em, mention_author=False)


    @command(name="serverinfo", help="Shows the details of your server")
    @cooldown(1, 5, BucketType.user)
    async def server_info(self, ctx):
        guild = ctx.guild

        # Many of these variables aren't necessary but since the embed has many fields, I didn't want the code to be messy
        created = guild.created_at.strftime("%d %B %Y at %I %p")
        emojis = guild.emojis
        members = guild.member_count
        owner = guild.owner
        level = guild.verification_level
        boost_level = guild.premium_tier
        large = guild.large
        subs = guild.premium_subscribers
        roles = len(ctx.guild.roles)

        em = discord.Embed(title=f"Here's the information I found on {ctx.guild.name}", color=colors.l_green)
        em.set_thumbnail(url=guild.icon_url)
        em.add_field(name='ID', value=f"`{guild.id}`", inline=False)
        em.add_field(name='Owner', value=owner, inline=False)
        em.add_field(name='Created on', value=created, inline=False)
        em.add_field(name='Is this server considered a big server?', value=checks.bool_str(large), inline=False)
        em.add_field(name='Member Count', value=members)
        em.add_field(name='Number of roles', value=roles - 1, inline=False)  # To ignore @everyone role
        em.add_field(name='Emojis', value=len(emojis), inline=False)
        em.add_field(name='Security Level', value=str(level).capitalize(), inline=False)
        em.add_field(name='Server Boosters', value=len(subs), inline=False)
        em.add_field(name='Server level', value=boost_level, inline=False)
        em.set_footer(text=f'Requested by {ctx.author.display_name}', icon_url=ctx.author.avatar_url)

        await ctx.reply(embed=em, mention_author=False)


    @command(name='roleinfo', help="Shows the permissions that a role has")
    @cooldown(1, 5, BucketType.user)
    async def role_info(self, ctx, role: discord.Role):
        if role not in ctx.guild.roles:
            await ctx.reply("I can't find that role in this server")
            return

        perms = role.permissions  # returns a list of permissions
        d_perms = ''  # d stands for decorated

        for perm in perms:  # Rewriting the perms in a more presentable manner
            if False not in perm:  # We only want to log the permissions that the role has
                perm = str(perm)
                if '_' in perm:
                    perm = perm.replace('_', ' ')
                if 'guild' in perm:
                    perm = perm.replace('guild', 'server')  # Since guilds are called servers in the GUI
                if '(' in perm:
                    perm = perm.replace("('", '')
                    perm = perm.replace("'", '')
                    perm = perm.replace(')', '')
                    perm = perm.replace(',', ' ')

                perm = perm.title()  # Capitalizing first letter of every word
                perm = perm.replace('True', '')
                d_perms += f"{perm}\n"

        em = discord.Embed(title='@' + role.name, color=role.color)  # I chose role.color, but that's a personal preference
        em.add_field(name='ID', value=role.id, inline=False)
        em.add_field(name="Permissions", value=d_perms, inline=False)
        em.add_field(name='Number of people that have this role', value=len(role.members), inline=False)
        em.add_field(name='Can everyone mention this role?', value=checks.bool_str(role.mentionable), inline=False)

        await ctx.reply(embed=em, mention_author=False)


    @command(name="steal", aliases=['stealemoji'], help="Steal an emoji")
    @cooldown(1, 5, BucketType.user)
    @has_permissions(manage_emojis=True)
    @bot_has_permissions(manage_emojis=True)
    async def steal(self, ctx, emoji_name, custom_emoji_name=None):
        """
        I'm not sure how most of this part works. I took this from a friend.
        """
        image = None

        if len(ctx.message.attachments) == 0:
            image = emoji_name
            emoji_name = None
            image_url = None

        if len(ctx.message.attachments) > 0:
            image_url = ctx.message.attachments[0].url
            custom_emoji_name = emoji_name

        image_url = None
        if image:
            try:
                try:
                    image = await discord.ext.commands.PartialEmojiConverter.convert(self, ctx=ctx, argument=image)
                except commands.BadArgument or commands.CommandError:
                    await ctx.reply("An error occured while stealing the emoji from that source. Sorry", mention_author=False)
                    return

                if custom_emoji_name:
                    emoji_name = custom_emoji_name
                else:
                    emoji_name = image.name

                image_url = image.url

            except commands.BadArgument:
                image_url = image

        if image_url is None:
            await ctx.reply("An error occured while stealing the emoji from that source. Sorry", mention_author=False)
            return

        try:
            response = requests.get(image_url, stream=True)
            if response.status_code == 200:
                with open(f"./emojis/{emoji_name}.gif", "wb") as img:
                    response.raw.decode_content = True
                    shutil.copyfileobj(response.raw, img)

            else:
                raise Exception(f"Bad status code uploading {emoji_name} received: {response.status_code}")

            with open(f"./emojis/{emoji_name}.gif", "rb") as image:
                try:
                    if isinstance(ctx, discord.Guild):
                        await ctx.create_custom_emoji(name=emoji_name, image=image.read())
                    else:
                        await ctx.message.guild.create_custom_emoji(name=emoji_name, image=image.read())

                    embed = discord.Embed(
                        title="Emoji added successfully",
                        colour=colors.l_green,
                        description=f"`:{emoji_name}:`"
                    )
                    embed.set_thumbnail(url=image_url)

                    await ctx.message.channel.send(embed=embed)

                except discord.errors.HTTPException as e:
                    if e.code == 400:
                        await ctx.reply("Only letters, numbers and underscores are allowed in emoji names.", mention_author=False)
                        return

                except Exception as e:
                    print(e)

        except requests.exceptions.MissingSchema:
            await ctx.reply(f"`{image_url}` doesn't seem like an emoji or an image", mention_author=False)


    @command(name='urban', aliases=['ud', 'urbandict'], help="Look up for a word on the Urban Dictionary")
    @cooldown(1, 5, BucketType.user)
    async def urban_dictionary(self, ctx, *, word):
        api = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"

        querymsg = {'term': word}  # term is the word that needs to be searched. in our case, *word*, the param

        headers = {
            'x-rapidapi-key': os.environ.get('urban_dict_key'),  # get your own key from rapidapi for free and paste it here instead of the whole os.environ thingy
            'x-rapidapi-host': 'mashape-community-urban-dictionary.p.rapidapi.com'
        }

        response = requests.request('GET', api, headers=headers, params=querymsg)
        response = response.json()  # This will be a very big dictionary, we need to 'decorate' it

        try:
            definition = response['list'][0]['definition']  # You can print the response to get an idea of why I did this
            example = response['list'][0]['example']

            for bracket in str(definition):
                if bracket == '[' or bracket == ']':
                    definition = definition.replace(bracket, '')

            for other_bracket in str(example):
                if other_bracket == '[' or other_bracket == ']':
                    example = example.replace(other_bracket, '')

            em = discord.Embed(title=word, color=colors.l_yellow)
            em.add_field(name='Top definition:', value=definition, inline=False)
            em.add_field(name='Example:', value=example)

            await ctx.reply(embed=em, mention_author=False)
        except KeyError:
            try:
                raw_dict = urbandict.define(word)  # returns a dictionary
                defintion = raw_dict[0]['def']
                example = raw_dict[0][str('example')]

                em = discord.Embed(name=word, color=colors.l_yellow)
                em.add_field(name='Top definition:', value=defintion, inline=False)
                em.add_field(name='Example:', value=example)
                em.set_footer(text="This result might not be very accurate")

                await ctx.reply(embed=em, mention_author=False)
            except KeyError:
                await ctx.reply("I couldn't find the defintion for that", mention_author=False)


    @command(name='reddit', aliases=['subreddit', 'getredditpost'], help='Gets a post from the subreddit provided')
    @cooldown(1, 3, commands.BucketType.user)
    async def get_reddit_post(self, ctx, *, subreddit):
        url = f'https://meme-api.herokuapp.com/gimme/{subreddit}'  # This api only sends posts with images or gifs.

        post = requests.get(url=url).json()
        # Check if the post is nsfw
        if 'nsfw' in post:  # Sometimes it raises KeyError
            if post['nsfw']:
                if not ctx.channel.is_nsfw():
                    await ctx.reply("The post I got from that subreddit is marked NSFW. I cannot send it here", mention_author=False)
                    return
        try:
            image = post['url']  # the image
            title = post['title']  # the title of the reddit post
            link = post['postLink']  # the link to the post

            em = discord.Embed(
                title=title,
                description=link,
                color=colors.orange
            )
            if len(em.title) > 256:
                em.title = "Title was too long for an embed."

            em.set_image(url=image)
            em.set_footer(
                text=f"👍 {post['ups']} | Author: u/{post['author']}")  # post['ups'] is the upvote count, post['author'] is the author

            await ctx.reply(embed=em, mention_author=False)

        except KeyError:
            if post["code"] == 400:
                if "no posts with images" in post["message"].lower():
                    await ctx.reply("That subreddit doesn't have any posts with images", mention_author=False)
                    return

            if post["code"] == 404:
                await ctx.reply("This subreddit has no posts or doesn't exist.", mention_author=False)
                return


    @command(name='csgo', aliases=['csgostats'], help="Get CSGO Stats of a Steam Account")
    @cooldown(1, 5, BucketType.user)
    async def get_csgo_stats(self, ctx, steam_profile_link=None):
        def check(message: discord.Message) -> bool:
            return message.author == ctx.author

        url = steam_profile_link

        if url is None:
            msg = await ctx.reply("Enter your Steam Profile URL. This message is active for 2 minutes", mention_author=False)
            try:
                await ctx.reply("To find your profile link, open steam in a browser, and go to your profile. Then copy the link and paste it here.", mention_author=False)
                message = await self.bot.wait_for('message', timeout=2 * 60, check=check)

                url = message.content.lower()

            except asyncio.TimeoutError:
                await msg.edit('This message is now inactive because you took too long to respond')
                return

        _id = checks.get_steam_id_from_url(url=url)
        if _id is None:
            await ctx.reply("I couldn't find your steam profile from that. Try running `help csgo`", mention_author=False)
            return

        key = os.environ.get('STEAM_API_KEY')
        stats = requests.get(f"http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v2/?appid=730&key={key}&steamid={_id}")

        if 'Internal Server Error' in stats.text:
            await ctx.reply("Uh-oh. Error.\nMaybe a Steam Profile with those details doesn't exist?\nMaybe they don't play CS:GO?\nMaybe their game details are private?", mention_author=False)
            return

        if stats.status_code == '500':  # Status code is 500 when profile not found or profile private
            await ctx.reply("I think your profile and/or game details are set to private. Make them public and try again", mention_author=False)
            return

        stats = stats.json()
        playerstats = stats['playerstats']
        gstats = playerstats['stats']  # game stats

        def get_pos(name):
            for i in range(0, len(gstats)):
                if gstats[i]['name'] == name:
                    return i

        def get_value(name):
            pos = get_pos(name)
            try:
                dict_ = gstats[pos]
                value = dict_['value']
                try:
                    return "{:,}".format(value)
                except TypeError:  # If the value is NoneType
                    return value
            except KeyError:
                pass

        def get_value_without_comma(name):
            pos = get_pos(name)
            try:
                dict_ = gstats[pos]
                value = dict_['value']
                return value
            except KeyError:
                pass

        kills = (get_value('total_kills'))
        deaths = (get_value('total_deaths'))

        _kills = get_value_without_comma('total_kills')
        _deaths = get_value_without_comma('total_deaths')
        kd = _kills / _deaths

        playtime = (get_value_without_comma('total_time_played'))
        playtime = playtime / 3600
        playtime = (round(playtime))

        games_won = (get_value('total_wins'))
        damage = (get_value('total_damage_done'))
        money = (get_value('total_money_earned'))
        knife = (get_value('total_kills_knife'))
        headshots = (get_value('total_kills_headshot'))
        grenade = get_value('total_kills_hegrenade')

        em = discord.Embed(
            title=f"CSGO Stats for {_id}",
            description=f"""
**Total Kills**: {kills}
**Total Deaths**: {deaths}
**K/D**: {str(kd)[0:5]}
**Total Damage**: {damage}
**Total Money Earned**: ${money}
**Actual Play Time**: {playtime} hours
**Matches Won (All game modes)**: {games_won}
*---------------------*
**Total Knife Kills**: {knife}
**Total Headshot Kills**: {headshots}
**Total Grenade Kills**: {grenade}
""",
            color=colors.l_green)
        await ctx.reply(embed=em, mention_author=False)


        @commands.command(name='csgodetail', aliases=['csgostatsdetail'], help='Get CSGO Stats of a Steam account')
        async def csgo_detail(self, ctx, steam_profile_link=None):
            """
            A lot of code from the get_csgo_stats is being repeated here, but meh
            """
            def check(message: discord.Message) -> bool:
                return message.author == ctx.author

            url = steam_profile_link

            if url is None:
                msg = await ctx.reply("Enter your Steam Profile URL. This message is active for 2 minutes", mention_author=False)
                await ctx.reply("To find your profile link, open steam in a browser, and go to your profile. Then copy the link and paste it here.", mention_author=False)
                try:
                    message = await self.client.wait_for('message', timeout=2 * 60, check=check)
                    url = message.content.lower()
                except asyncio.TimeoutError:
                    await msg.edit('This message is now inactive because you took too long to respond')
                    return

            _id = await self.get_id_from_url(url=url)
            if _id is None:
                await ctx.reply("I couldn't find your steam profile from that. Try running `help csgo`", mention_author=False)
                return

            key = os.environ.get('STEAM_API_KEY')
            stats = requests.get(f"http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v2/?appid=730&key={key}&steamid={_id}")

            if 'Internal Server Error' in stats.text:
                await ctx.reply("Uh-oh. Error.\nMaybe a Steam Profile with those details doesn't exist?\nMaybe they don't play CS:GO?\nMaybe their game details are private?", mention_author=False)
                return

            if stats.status_code == '500':  # Status code is 500 when profile not found or profile private
                await ctx.reply("I think your profile and/or game details are set to private. Make them public and try again", mention_author=False)
                return

            stats = stats.json()
            playerstats = stats['playerstats']
            gstats = playerstats['stats']  # game stats

            def get_pos(name):
                for i in range(0, len(gstats)):
                    if gstats[i]['name'] == name:
                        return i

            def get_value(name):
                pos = get_pos(name)

                if pos is None:
                    return None

                try:
                    dict_ = gstats[pos]
                    value = dict_['value']
                    try:
                        return "{:,}".format(value)
                    except TypeError:  # If the value is NoneType
                        return value
                except KeyError:
                    pass

            # Pistol
            glock = (get_value('total_kills_glock'))
            usp = (get_value('total_kills_hkp2000'))  # USP is called hkp2000 in the json returned by the API
            dual = (get_value('total_kills_elite'))  # Dual Berettas are called elite in the json returned by the API
            p250 = (get_value('total_kills_p250'))
            tec9 = (get_value('total_kills_tec9'))
            fiveseven = (get_value('total_kills_fiveseven'))
            deag = (get_value('total_kills_deagle'))

            # Smg
            mac10 = (get_value('total_kills_mac10'))
            mp9 = (get_value('total_kills_mp9'))
            mp7 = (get_value('total_kills_mp7'))
            ump = (get_value('total_kills_ump45'))
            p90 = (get_value('total_kills_p90'))
            bizon = (get_value('total_kills_bizon'))

            # Shotgun
            nova = (get_value('total_kills_nova'))
            xm1014 = (get_value('total_kills_xm1014'))
            sawed = (get_value('total_kills_sawdoff'))
            mag7 = (get_value('total_kills_mag7'))

            # Rifle
            galil = (get_value('total_kills_galilar'))
            famas = (get_value('total_kills_famas'))
            ak47 = (get_value('total_kills_ak47'))
            m4 = (get_value('total_kills_m4a1'))
            ssg08 = (get_value('total_kills_ssg08'))
            sg553 = (get_value('total_kills_sg556'))  # sg553 is called ss556 in the json returned by the API
            aug = (get_value('total_kills_aug'))
            awp = (get_value('total_kills_awp'))
            g3sg1 = (get_value('total_kills_g3sg1'))
            scar20 = (get_value('total_kills_scar20'))

            # Misc
            negev = (get_value('total_kills_negev'))
            m249 = (get_value('total_kills_m249'))
            zeus = (get_value('total_kills_taser'))

            em = discord.Embed(
                title=f"CSGO Stats for {_id}",
                color=colors.l_green
            )
            em.add_field(
                name="__Terrorist Weapons__",
                value=f"""
    **Glock**: {glock}
    **Tec-9**: {tec9}
    **Mac-10**: {mac10}
    **Sawed-off**: {sawed}
    **Galil AR**: {galil}
    **AK-47**: {ak47}
    **SG553**: {sg553}
    **G3SG1**: {g3sg1}
                """,
                inline=False
            )
            em.add_field(
                name="__Counter-Terrorist Weapons__",
                value=f"""
    **USP/P2000**: {usp}
    **Five-Seven**: {fiveseven}
    **MP9**: {mp9}
    **Mag 7**: {mag7}
    **FAMAS**: {famas}
    **M4**: {m4}
    **AUG**: {aug}
    **SCAR-20**: {scar20}
                """,
                inline=False
            )
            em.add_field(
                name="__Common Weapons__",
                value=f"""
    **Dual Berettas**: {dual}
    **P250**: {p250}
    **Desert Eagle/R8**: {deag}
    **MP7/MP5**: {mp7}
    **UMP-45**: {ump}
    **P90**: {p90}
    **PP Bizon**: {bizon}
    **Nova**: {nova}
    **XM-1014**: {xm1014}
    **SSG-08**: {ssg08}
    **AWP**: {awp}
    **Negev**: {negev}
    **M249**: {m249}
    **Zeus x27**: {zeus}
                """,
                inline=False
            )
            await ctx.reply(embed=em, mention_author=False)


    @commands.Cog.listener()
    async def on_message_delete(self, message):
        channel = str(message.channel.id)
        del_msg[channel] = {}
        del_msg[channel]['content'] = message.content
        del_msg[channel]['author'] = message.author
        del_msg[channel]['time'] = datetime.now(pytz.utc)  # This will be used for the timestamp

        if len(message.attachments) > 0:
            del_msg[channel]['attachment'] = str(message.attachments[0].url)
        else:
            del_msg[channel]['attachment'] = None

        if len(message.embeds) > 0:
            del_msg[channel]['embed'] = message.embeds[0]
        else:
            del_msg[channel]['embed'] = None


    @commands.command(name='snipe', help='Check the last deleted message in the channel')
    async def snipe(self, ctx):
        try:
            msg_content = del_msg[str(ctx.channel.id)]['content']
            if msg_content == '':  # If the message had no text, it means that it had an attachment. Since the message is deleted, we can't retrieve that.
                msg_content = "There was an image or an embed in the deleted message that couldn't be loaded, but here's the url"

            em = discord.Embed(
                description=msg_content,
                color=colors.l_green,
                timestamp=del_msg[str(ctx.channel.id)]['time']
            )
            em.set_author(name=f"{del_msg[str(ctx.channel.id)]['author']} said:", icon_url=del_msg[str(ctx.channel.id)]['author'].avatar_url)

            if del_msg[str(ctx.channel.id)]['attachment'] is not None:
                em.description = f"{msg_content} \n\n [**Attachment**]({del_msg[str(ctx.channel.id)]['attachment']})"

            if del_msg[str(ctx.channel.id)]['embed'] is not None:
                em.description = f"{msg_content} \n\n The deleted message had this embed:"

            await ctx.reply(embed=em, mention_author=False)

            if del_msg[str(ctx.channel.id)]['embed'] is not None:  # Yes, same check 2nd time. I needed it to send the embed after the main embed
                await ctx.send(embed=del_msg[str(ctx.channel.id)]['embed'])

        except discord.errors.Forbidden or discord.Forbidden:
            await ctx.reply("I don't have the embed links permission. I need that.", mention_author=False)

        except KeyError:
            await ctx.reply("There are no recently deleted messages", mention_author=False)


    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        edit_msg[str(before.channel.id)] = {}

        edit_msg[str(before.channel.id)]['before'] = before.content
        edit_msg[str(before.channel.id)]['after'] = after.content
        edit_msg[str(before.channel.id)]['author'] = before.author
        edit_msg[str(before.channel.id)]['time'] = datetime.now(pytz.utc)  # This will be used for the timestamp


    @commands.command(name='editsnipe', aliases=['es'], help='Check the last edited message in the channel')
    async def editsnipe(self, ctx):
        try:
            em = discord.Embed(
                color=colors.l_green,
                timestamp=edit_msg[str(ctx.channel.id)]['time']
            )
            em.set_author(
                name=f"{edit_msg[str(ctx.channel.id)]['author']} said:",
                icon_url=edit_msg[str(ctx.channel.id)]['author'].avatar_url
            )
            em.add_field(
                name='Before',
                value=edit_msg[str(ctx.channel.id)]['before'],
                inline=False
            )  # If the embed has 2 fields, using inline=False only once is enough)
            em.add_field(
                name='After',
                value=edit_msg[str(ctx.channel.id)]['after']
            )

            await ctx.reply(embed=em, mention_author=False)
        except KeyError:
            await ctx.reply("There are no recently edited messages", mention_author=False)


def setup(bot):
    bot.add_cog(Utility(bot))
    print("Utility cog loaded")
