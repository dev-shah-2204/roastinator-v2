"""
If you want to know more about discord.py, I recommend https://discordpy.readthedocs.io/en/latest
"""
import os
import random
import discord
import hex_colors

from discord.ext import commands, tasks
from discord.ext.commands import BucketType, CommandOnCooldown


prefix = commands.when_mentioned_or('-') #Dont copy this stuff
tprefix = '>' #Dont copy this stuff


#Defining our client
client = commands.Bot(command_prefix = prefix, intents = discord.Intents.all(), case_insensitive = True)
client.remove_command('help')

#You don't need to copy this stuff#########
                                         ##
heroku = True                            ##
if heroku == True:                       ##
    token = os.environ.get('token')      ##
else:                                    ##
    import myToken                       ## 
    token = myToken.token                ##
                                         ##
###########################################


owner_id = client.owner_id

#Loading cogs (extensions)
error_handling = True
event_cog_list = [
            'cogs.events.on_message',
            'cogs.events.on_ready'
]

command_cog_list = [
                'cogs.commands.help',
                'cogs.commands.bot_stats',
                'cogs.commands.moderation',
                'cogs.commands.snipe',
                'cogs.commands.utility',
                'cogs.commands.developer_commands'
]

for event_cog in event_cog_list: #Running a loop for all event cogs
    if __name__ == '__main__':
        client.load_extension(event_cog)

for command_cog in command_cog_list: #Running a loop for all command cogs
    if __name__ == '__main__':
        client.load_extension(command_cog)

if error_handling == True:
    client.load_extension('cogs.events.on_command_error')


    

#RUN
client.run(token) #Enter your token here
