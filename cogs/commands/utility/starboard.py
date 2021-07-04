import discord 
import hex_colors 

from cache import star_cache
from db import *
from discord.ext import commands

db = database.cursor()
class StarboardCommands(commands.Cog):
    def __init__(self, client):
        self.client = client 

    @commands.group(name='starboard', help='Commands related to starboard', invoke_without_command=True)
    @commands.has_permissions(manage_messages=True)
    async def starboard_commands(self, ctx):
        em = discord.Embed(
            title="Starboard Commands",
            description="""
`channel` - Set the starboard channel
`enable`  - Enable starboard for the server
`disable` - Disable starboard for the server
            """,
            color=hex_colors.l_yellow)

        db.execute(f"SELECT _status FROM Starboard WHERE guild = '{ctx.guild}'")
        status = await get_data(db=db)
        if status == 'enabled':
            db.execute(f"SELECT _channel FROM Starboard WHERE guild = '{ctx.guild}'")
            channel = await get_data(db=db)
            
            em.add_field(
                name='Starboard channel:',
                value=f'<@&{channel[0]}>'
            )
        else:
            em.set_footer(text="Starboard hasn't been setup in this server yet")

        await ctx.send(embed=em)

    @starboard_commands.command(name='channel', help="Set the starboard channel")
    async def channel(self, ctx, channel:discord.TextChannel):
        try:
            db.execute(f"INSERT INTO Starboard(guild, _channel, _status) VALUES ('{ctx.guild.id}','{channel.id}','enabled')")
        except:
            db.execute(f"UPDATE Starboard SET _channel = '{channel.id}' WHERE guild = '{ctx.guild.id}'")

        star_cache[str(ctx.guild.id)] = channel.id
        database.commit()
        await ctx.send(f"Starboard set to <#{channel.id}>")

    @starboard_commands.command(name='disable', help="Disable starboard")
    async def disable_starboard(self, ctx):
        try:
            db.execute(f"UPDATE Starboard SET _status = 'disabled' WHERE guild = '{ctx.guild}'")
            database.commit()
            await ctx.send("Disabled starboard")
        except:
            await ctx.send("Starboard was never enabled for this server")

    @starboard_commands.command(name='enable', help="Enable starboard")
    async def enable_starboard(self, ctx):
        try:
            db.execute(f"UPDATE Starboard SET _status = 'enabled' WHERE guild = '{ctx.guild}'")
            database.commit()
            await ctx.send("Enabled starboard for this server")
        except:
            await ctx.send("Starboard has not been set in this server. First run the `starboard channel` command")


def setup(client):
    client.add_cog(StarboardCommands(client))
    print('StarboardCommands')