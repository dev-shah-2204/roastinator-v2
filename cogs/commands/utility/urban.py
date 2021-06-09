import discord
import random
import os
import requests
import json
import urbandict
import hex_colors

from discord.ext import commands

class UrbanDictionary(commands.Cog):
    def __init__(self, client):
        self.client = client

    """
    Note: Both the API and the Library have bugs. They are not always able to find the definition even if they are on the urbandictionary website
    """

    @commands.command(name = 'urban', aliases = ['ud','urbandict'])
    async def urban(self, ctx, *, word):
        api = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"

        querymsg = {'term':word} #term is the word that needs to be searched. in our case, *word*, the param

        headers = {
            'x-rapidapi-key': os.environ.get('urban_dict_key'), #get your own key from rapidapi for free and paste it here instead of the whole os.environ thingy
            'x-rapidapi-host': 'mashape-community-urban-dictionary.p.rapidapi.com'
        }

        response = requests.request('GET', api, headers = headers, params = querymsg)
        response = response.json() #This will be a very big dictionary, we need to 'decorate' it

        try:
            definition = response['list'][0]['definition'] #You can print the response to get an idea of why I did this
            example = response['list'][0]['example']

            for bracket in str(definition):
                if bracket == '[' or bracket == ']':
                    definition = definition.replace(bracket,'')

            for other_bracket in str(example):
                if other_bracket == '[' or other_bracket == ']':
                    example = example.replace(other_bracket, '')

            em = discord.Embed(title = word, color = random.choice(hex_colors.colors))
            em.add_field(name = 'Top definition:', value = definition, inline = False)
            em.add_field(name = 'Example:', value = example)

            await ctx.send(embed = em)
        except:
            try:
                raw_dict = urbandict.define(word) #returns a dictionary
                defintion = raw_dict[0]['def']
                example = raw_dict[0][str('example')]

                em = discord.Embed(name = word, color = random.choice(hex_colors.colors))
                em.add_field(name = 'Top definition:', value = defintion, inline = False)
                em.add_field(name = 'Example:', value = example)
                em.set_footer(text = "I couldn't find the defintion using the primary API, so this might not be very accurate")

                await ctx.send(embed = em)
            except:
                await ctx.send("I couldn't find the defintion because both the API and the library are broken")

def setup(client):
    client.add_cog(UrbanDictionary(client))
    print('UrbanDictionary')
