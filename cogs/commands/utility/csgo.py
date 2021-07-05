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
        if 'profiles' in url:
            url = url.replace('https://','')
            url = url.replace('steamcommunity.com/profiles/','')
            url = url.strip('/')
            return url

        elif '/id/' in url:
            url = url.replace('https://','')
            url = url.replace('steamcommunity.com/id/','')
            url = url.strip('/')
        

        try:
            _id = int(url) #To check if they entered the ID or the vanity URL
        except:
            _id = requests.get(f"http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={os.environ.get('STEAM_API_KEY')}&vanityurl={url}").json() #To get ID from vanity URL

        return _id['response']['steamid']
        


    @commands.command(name='csgo', aliases=['csgostats'], help="Get CSGO Stats of a Steam Account")
    async def get_csgo_stats(self, ctx, steam_profile_link=None):
        def check(message:discord.Message) -> bool:
            return message.author == ctx.author 

        url = steam_profile_link

        if url == None:
            try:
                msg = await ctx.send("Enter your Steam Profile URL. This message is active for 2 minutes")
                await ctx.send("To find your profile link, open steam in a browser, and go to your profile. Then copy the link and paste it here.")
                message = await self.client.wait_for('message', timeout=2*60, check=check)

                url = message.content.lower()

            except asyncio.TimeoutError:
                await msg.edit('This message is now inactive because you took too long to respond')
                return 

        _id = await self.get_id_from_url(url=url)  

        stats = requests.get(f"http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v2/?appid=730&key={os.environ.get('STEAM_API_KEY')}&steamid={_id}")
        if stats.status_code == 500:
            await ctx.send("I think your profile and/or game details are set to private. Make them public and try again")
            return 

        stats = stats.json()
                
        json = stats['playerstats']
        gstats = json['stats'] #game stats
        def get_pos(name):
            for i in range(0, len(gstats)+1):
                if gstats[i]['name'] == name:
                    return i

        def get_value(name):
            pos = get_pos(name)
            dict_ = gstats[pos]
            return dict_['value']

        kills = "{:,}".format(get_value('total_kills'))
        deaths = "{:,}".format(get_value('total_deaths'))
        kd = int(get_value('total_kills'))/int(get_value('total_deaths'))
        playtime = int(get_value('total_time_played'))/3600
        playtime = "{:,}".format(round(playtime))
        games_won = "{:,}".format(get_value('total_wins'))
        damage = "{:,}".format(get_value('total_damage_done'))
        money = "{:,}".format(get_value('total_money_earned'))
        knife = "{:,}".format(get_value('total_kills_knife'))
        headshots = "{:,}".format(get_value('total_kills_headshot'))
        grenade = "{:,}".format(get_value('total_kills_hegrenade'))

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
        def check(message:discord.Message) -> bool:
            return message.author == ctx.author 

        url = steam_profile_link

        if url == None:
            try:
                msg = await ctx.send("Enter your Steam Profile URL. This message is active for 2 minutes")
                await ctx.send("To find your profile link, open steam in a browser, and go to your profile. Then copy the link and paste it here.")
                message = await self.client.wait_for('message', timeout=2*60, check=check)

                url = message.content.lower()

            except asyncio.TimeoutError:
                await msg.edit('This message is now inactive because you took too long to respond')
                return 

        _id = await self.get_id_from_url(url=url)  

        stats = requests.get(f"http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v2/?appid=730&key={os.environ.get('STEAM_API_KEY')}&steamid={_id}")
        if stats.status_code == 500:
            await ctx.send("I think your profile and/or game details are set to private. Make them public and try again")
            return 

        stats = stats.json()
                
        json = stats['playerstats']
        gstats = json['stats'] #game stats
        def get_pos(name):
            for i in range(0, len(gstats)+1):
                if gstats[i]['name'] == name:
                    return i

        def get_value(name):
            pos = get_pos(name)
            dict_ = gstats[pos]
            return dict_['value']

        #Pistol
        glock = "{:,}".format(get_value('total_kills_glock'))
        usp = "{:,}".format(get_value('total_kills_hkp2000'))
        dual = "{:,}".format(get_value('total_kills_elite'))
        p250 = "{:,}".format(get_value('total_kills_p250'))
        tec9 = "{:,}".format(get_value('total_kills_tec9'))
        fiveseven = "{:,}".format(get_value('total_kills_fiveseven'))
        deag = "{:,}".format(get_value('total_kills_deagle'))     

        #Smg
        mac10 = "{:,}".format(get_value('total_kills_mac10'))
        mp9 = "{:,}".format(get_value('total_kills_mp9'))
        mp7 = "{:,}".format(get_value('total_kills_mp7'))
        ump = "{:,}".format(get_value('total_kills_ump45'))
        p90 = "{:,}".format(get_value('total_kills_p90'))
        bizon = "{:,}".format(get_value('total_kills_bizon'))

        #Shotgun
        nova = "{:,}".format(get_value('total_kills_nova'))
        xm1014 = "{:,}".format(get_value('total_kills_xm1014'))
        sawed = "{:,}".format(get_value('total_kills_sawdoff'))
        mag7 = "{:,}".format(get_value('total_kills_mag7'))

        #Rifle
        galil = "{:,}".format(get_value('total_kills_galilar'))
        famas = "{:,}".format(get_value('total_kills_famas'))
        ak47 = "{:,}".format(get_value('total_kills_ak47'))
        m4 = "{:,}".format(get_value('total_kills_m4a1'))
        ssg08 = "{:,}".format(get_value('total_kills_ssg08'))
        sg553 = "{:,}".format(get_value('total_kills_sg553'))
        aug = "{:,}".format(get_value('total_kills_aug'))
        awp = "{:,}".format(get_value('total_kills_awp'))
        g3sg1 = "{:,}".format(get_value('total_kills_g3sg1'))
        scar20 = "{:,}".format(get_value('total_kills_scar20'))

        #Misc
        negev = "{:,}".format(get_value('total_kills_negev'))
        m249 = "{:,}".format(get_value('total_kills_m249'))
        zeus = "{:,}".format(get_value('total_kills_taser'))        

        em = discord.Embed(
            title=f"CSGO Stats for {_id}",
            color=random.choice(hex_colors.colors)
        )
        em.add_field(
            name="Terrorist Weapons",
            value=f"""
**Glock**: {glock}
**Tec-9**: {tec9}
-
**Mac-10**: {mac10}
-
**Sawed-off**: {sawed}
-
**Galil AR**: {galil}
**AK-47**: {ak47}
**SG553**: {sg553}
**G3SG1**: {g3sg1}
            """
        )
        em.add_field(
            name="Counter-Terrorist Weapons",
            value=f"""
**USP/P2000*: {usp}
**Five-Seven**: {fiveseven}
-
**MP9**: {mp9}
-
**Mag 7**: {mag7}
-
**FAMAS**: {famas}
**M4**: {m4}
**AUG**: {aug}
**SCAR-20**: {scar20}
            """
        )
        em.add_field(
            name="Common Weapons",
            value=f"""
**Dual Berettas**: {dual}
**P250**: {p250}
**Desert Eagle/R8**: {deagle}
-
**MP7**: {mp7}
**P90**: {p90}
**PP Bizon**: {bizon}
-
**Nova**: {nova}
**XM-1014**: {xm1014}
-
**SSG-08**: {ssg08}
**AWP**: {awp}
-
**Negev**: {negev}
**M249**: {m249}
-
**Zeus x27**: {zeus}
****
            """
        )
        await ctx.send(embed=em)



def setup(client):
    client.add_cog(CSGOStats(client))
    print('CSGOStats')