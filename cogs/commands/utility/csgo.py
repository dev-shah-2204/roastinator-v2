import discord
import requests
import hex_colors
import asyncio
import os
import random

from discord.ext import commands


class CSGOStats(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def get_id_from_url(self, url):
        url = url.replace('https://', '')
        url = url.replace('steamcommunity.com/profiles/', '')
        url = url.replace('steamcommunity.com/id/', '')
        url = url.strip('/')

        try:
            _id = int(url)  # If the user doesn't have a vanity url
            return _id
        except ValueError:
            _id = requests.get(f"http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={os.environ.get('STEAM_API_KEY')}&vanityurl={url}").json()  # To get ID from vanity URL

        try:
            return _id['response']['steamid']
        except KeyError:
            return None

    @commands.command(name='csgo', aliases=['csgostats'], help="Get CSGO Stats of a Steam Account")
    async def get_csgo_stats(self, ctx, steam_profile_link=None):
        def check(message: discord.Message) -> bool:
            return message.author == ctx.author

        await ctx.send("This command is under maintainence")
        return
        
        url = steam_profile_link

        if url is None:
            try:
                msg = await ctx.send("Enter your Steam Profile URL. This message is active for 2 minutes")
                await ctx.send("To find your profile link, open steam in a browser, and go to your profile. Then copy the link and paste it here.")
                message = await self.client.wait_for('message', timeout=2 * 60, check=check)

                url = message.content.lower()

            except asyncio.TimeoutError:
                await msg.edit('This message is now inactive because you took too long to respond')
                return

        _id = await self.get_id_from_url(url=url)
        if _id is None:
            await ctx.send("I couldn't find your steam profile from that. Try running `help csgo`")
            return

        key = os.environ.get('STEAM_API_KEY')
        stats = requests.get(f"http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v2/?appid=730&key={key}&steamid={_id}")

        if 'Internal Server Error' in stats.text:
            await ctx.send("Uh-oh. Error.\nMaybe a Steam Profile with those details doesn't exist?\nMaybe they don't play CS:GO?\nMaybe their game details are private?")
            return

        if stats.status_code == '500':  # Status code is 500 when profile not found or profile private
            await ctx.send("I think your profile and/or game details are set to private. Make them public and try again")
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
            color=random.choice(hex_colors.colors)
        )

        await ctx.send(embed=em)

    @commands.command(name='csgodetail', aliases=['csgostatsdetail'], help='Get CSGO Stats of a Steam account')
    async def csgo_detail(self, ctx, steam_profile_link=None):
        await ctx.send("This command is under maintainence")
        return
    
        def check(message: discord.Message) -> bool:
            return message.author == ctx.author

        url = steam_profile_link

        if url is None:
            try:
                msg = await ctx.send("Enter your Steam Profile URL. This message is active for 2 minutes")
                await ctx.send("To find your profile link, open steam in a browser, and go to your profile. Then copy the link and paste it here.")
                message = await self.client.wait_for('message', timeout=2 * 60, check=check)

                url = message.content.lower()

            except asyncio.TimeoutError:
                await msg.edit('This message is now inactive because you took too long to respond')
                return

        _id = await self.get_id_from_url(url=url)
        if _id is None:
            await ctx.send("I couldn't find your steam profile from that. Try running `help csgo`")
            return

        key = os.environ.get('STEAM_API_KEY')
        stats = requests.get(f"http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v2/?appid=730&key={key}&steamid={_id}")

        if stats.status_code == 500:  # Error code 500 is a generic status code sent when the website/API can't pin-point the problem
            await ctx.send("I think your profile and/or game details are set to private. Make them public and try again")
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

        # Pistol
        glock = (get_value('total_kills_glock'))
        usp = (get_value('total_kills_hkp2000'))
        dual = (get_value('total_kills_elite'))
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
        sg553 = (get_value('total_kills_sg553'))
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
            color=random.choice(hex_colors.colors)
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
**MP7**: {mp7}
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
        await ctx.send(embed=em)


def setup(client):
    client.add_cog(CSGOStats(client))
    print('CSGOStats')
