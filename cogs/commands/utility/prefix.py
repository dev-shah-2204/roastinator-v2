import discord
import mysql.connector
import os
import hex_colors

from prefix_cache import cache
from db import database
from discord.ext import commands

db = database.cursor(buffered = True)

class Prefix(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name = 'prefix', aliases = ['setprefix','changeprefix'], help = 'Change the prefix to which the bot responds')
    @commands.has_permissions(manage_guild = True)
    async def change_prefix(self, ctx, newPrefix:str = None):
        if len(newPrefix) > 5: #You can change this limit as per your wish
            await ctx.send("Prefix cannot be longer than 5 characters")
            return

        else:
            try:
                db.execute("INSERT INTO Prefix (guild, prefix) VALUES (%s, %s)", (str(ctx.guild.id), newPrefix))
                database.commit()
            except: #If the guild already exists in the database (most likely it is)
                db.execute(f"UPDATE Prefix SET prefix = '{newPrefix}' WHERE guild = '{ctx.guild.id}'")
                database.commit()

            em = discord.Embed(title = 'Prefix changed', description = f'New prefix: `{newPrefix}`', color = hex_colors.l_green)
            await ctx.send(embed = em)

            #Fixing cache
            cache[str(ctx.guild.id)] = newPrefix


def setup(client):
    client.add_cog(Prefix(client))
    print('Prefix')
