import discord
import random
import sys
import os
import re

from discord.ext import commands
from discord.ext.commands import CommandOnCooldown, BucketType
from .. import hex_colors

      ######
    ##########
   #####      ##
#######        ##
#######       ###         AAAAAAAA   MMMMMMMMM    OOOOOO   GGGGG    U     U   SSSSSS
###############          AAA   AAA  MM  MM  MM   OO   OO  GG       UU    UU  SS
###############          AAAAAAAAA  MM  MM  MM   OO   OO  GG  GGG  UU    UU  SSSSSSS
###############          AAA   AAA  MM      MM   OO   OO  GG   GG  UU    UU        S
   ###########           AAA   AAA  MM      MM   OOOOOOO  GGGGGG   UUUUUUUU  SSSSSSS
   ####   ####     
   

def bool_str(variable): #Function to convert boolean values to string: Yes/No
    if variable == True:
        return 'Yes'
    if variable == False:
        return 'No'


class Utility(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name = 'avatar', aliases = ['av'], help = "Show a user's avatar in full size")
    async def avatar(self, ctx, member:discord.Member = None):
        if member == None:
            member = ctx.author
        
        try:
            download_link = f"Download as [png]({member.avatar_url_as(format = 'png')}) | [jpeg]({member.avatar_url_as(format = 'jpeg')}) | [gif]({member.avatar_url_as(format = 'gif')})"
        except:
            download_link = f"Download as [png]({member.avatar_url_as(format = 'png')}) | [jpeg]({member.avatar_url_as(format = 'jpeg')}) | [webp]({member.avatar_url_as(format = 'webp')})"

        em = discord.Embed(title = f"{member.display_name}'s avatar", description = download_link, color = random.choice(hex_colors.colors))
        em.set_image(url = member.avatar_url)
        em.set_footer(text = f'Requested by {ctx.author.display_name}', icon_url = ctx.author.avatar_url)

        await ctx.send(embed = em)



    @commands.command(name = 'python', aliases = ['py'], help = 'Run a python code line in discord', usage = '<code>')
    @commands.cooldown(1, 10, BucketType.user)
    async def python_code(self, ctx, *, code):
        if 'import' in code:
            await ctx.send("Hey hey! You cannot import libraries yet.")
            return

        if 'quit(' in code or 'exit(' in code or 'input(' in code or 'sys.' in code or 'os.' in code: #So that they cannot do anything to our computer or turn off the bot
            await ctx.send("Yeah really smart, but you're not the only one who's smart xD")
            return

        while_loops = re.search(r'while[\s\w_\s]+==[\sTrue:False:]', code) #Checking for while loops
        for_loops = re.search(r'for[\s\w_\s]+in[\s\w_(,)\s]+:', code) #Checking for for loops (for for xD)
        
        if 'open(' in code or 'close(' in code: #We don't want people to access our files
            await ctx.send("You cannot open or close files")
            return

        if while_loops or for_loops or 'while True:' in code:
            await ctx.send("Come on you can't run loops here. If you really want to, you can try https://repl.it")
            return


        sys.stdout = open('cogs/commands/code_run_by_users.txt', 'w')#Output will be written in this file instead of terminal
        exec(code)
        sys.stdout.close()#If we don't close, the file is active and the data isn't saved
        
        return_code = open('cogs/commands/code_run_by_users.txt', 'r')
        return_code_string = return_code.read()
        return_code.close()

        await ctx.send(f"```\n{return_code_string}\n```")
 

    @commands.command(name = 'userinfo', aliases = ['whois'], help = 'Shows the details of a member', usage = '[member]')
    @commands.cooldown(1, 10, BucketType.user)
    async def whois(self, ctx, member:discord.Member = None):
        if member == None:
            member = ctx.author

        created = member.created_at.strftime("%d %B %Y at %I %p")
        id = member.id #id is a keyword in python but we can use it as a variable name too.
        joined = member.joined_at.strftime("%d %B %Y at %I %p")
      
        member_role_list = []
        for role in ctx.guild.roles: #In order to present the roles in a decorative way
            if role in member.roles and role.name != '@everyone': #Because it logs @everyone as @@everyone
                member_role_list.append(role.id)

        roles = "@everyone " #@everyone is a default role
        for member_role in member_role_list:
            roles += f"<@&{member_role}> "


        em = discord.Embed(title = f"Found information for {member}", color = random.choice(hex_colors.colors))
        em.set_thumbnail(url = member.avatar_url)
        em.add_field(name = "ID", value = id, inline = False)
        em.add_field(name = "Account Created on", value = created, inline = False)
        em.add_field(name = "Joined Server on", value = joined, inline = False)
        em.add_field(name = "Roles in this Server", value = roles, inline = False)
        em.set_footer(text = f"Requested by {ctx.author.nick}", icon_url = ctx.author.avatar_url)
        
        await ctx.send(embed = em)
        

    @commands.command(name = 'serverinfo', help = 'Information about the server', usage = '')
    @commands.cooldown(1, 10, BucketType.guild)
    async def serverinfo(self, ctx):
        guild = server = ctx.guild

        #Many of these variables aren't necessary but since the embed has many fields, I didn't want the code to be messy
        created = server.created_at.strftime("%d %B %Y at %I %p")
        emoji_limit = server.emoji_limit
        emojis = server.emojis
        members = server.member_count
        owner = server.owner
        level = server.verification_level
        region = server.region
        boost_level = server.premium_tier
        large = server.large
        
        roles = len(ctx.guild.roles)

        subs = server.premium_subscribers

        boosters = ""
        for person in subs:
            boosters += f'{person.mention} '

        if boosters == "":
            boosters = 'None'

        em = discord.Embed(title = f"Here's the information I found on {ctx.guild.name}", color = random.choice(hex_colors.colors))
        em.set_thumbnail(url = server.icon_url)
        em.add_field(name = 'ID', value = server.id, inline = False)
        em.add_field(name = 'Owner', value = owner, inline = False)
        em.add_field(name = 'Server Region', value = str(region).capitalize(), inline = False)
        em.add_field(name = 'Created on', value = created, inline = False)
        em.add_field(name = 'Is this server considered a big server?', value = bool_str(large), inline = False)
        em.add_field(name = 'Member Count', value = members)
        em.add_field(name = 'Number of roles', value = roles-1, inline = False) #To ignore @everyone role
        em.add_field(name = 'Security Level', value = level, inline = False)
        em.add_field(name = 'Server Boosters', value = boosters, inline = False)
        em.add_field(name = 'Server level', value = boost_level, inline = False)
        em.set_footer(text = f'Requested by {ctx.author}', icon_url = ctx.author.avatar_url)

        await ctx.send(embed = em)

    
    @commands.command(name = 'roleinfo', aliases = ['ri'], help = 'Shows information about a role', usage = '<role>')
    async def role_info(self, ctx, role:discord.Role):
        if role not in ctx.guild.roles:
            await ctx.send("I can't find that role in this server..")
            return

        perms = role.permissions

        d_perms = '' #d stands for decorated

        for perm in perms:
            if not False in perm: #We only want to log the permissions that the role has
                perm = str(perm)
                if '_' in perm:
                    perm = perm.replace('_',' ')
                if 'guild' in perm:
                    perm = perm.replace('guild','server') #Since guilds are called servers in the GUI
                if '(' in perm:
                    perm = perm.replace("('",'')
                    perm = perm.replace("'",'')
                    perm = perm.replace(')','')
                    perm = perm.replace(',',' ')

                perm = perm.title() #Capitalizing first letter of every word
                perm = perm.replace('True',':ballot_box_with_check:')
                perm = perm.replace('random string','')
                d_perms += f"{perm}\n"


        em = discord.Embed(title = '@'+role.name, color = role.color) #I chose role.color, but that's a personal preference
        em.add_field(name = 'ID', value = role.id, inline = False)
        em.add_field(name = "Permissions", value = d_perms, inline = False)
        em.add_field(name = 'Number of people that have this role', value = len(role.members), inline = False)
        em.add_field(name = 'Can everyone mention this role?', value = bool_str(role.mentionable), inline = False)

        await ctx.send(embed = em)
    

def setup(client):
    client.add_cog(Utility(client))
    print("Utility Command cog loaded")
