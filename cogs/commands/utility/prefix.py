import discord
import mysql.connector
import os
import hex_colors

from cache import prefix_cache
from db import *
from discord.ext import commands



class Prefix(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='prefix', aliases=['setprefix','changeprefix'], help='Change the prefix to which the bot responds')
    @commands.has_permissions(manage_guild=True)
    async def change_prefix(self, ctx, new_prefix:str=None):
        cache = prefix_cache
        if len(new_prefix) > 5: #You can change this limit as per your wish
            await ctx.send("Prefix cannot be longer than 5 characters")
            return

        else:
            try:
                db.execute("INSERT INTO Prefix (guild, prefix) VALUES (%s, %s)", (str(ctx.guild.id), new_prefix))
                database.commit()
            except: #If the guild already exists in the database (most likely it is)
                db.execute(f"UPDATE Prefix SET prefix = '{new_prefix}' WHERE guild = '{ctx.guild.id}'")
                database.commit()

            em = discord.Embed(
                title='Prefix changed', 
                description=f'New prefix: `{new_prefix}`',
                color=hex_colors.l_green
                )
            await ctx.send(embed=em)

            #Fixing cache
            cache[str(ctx.guild.id)] = new_prefix


def setup(client):
    client.add_cog(Prefix(client))
    print('Prefix')
