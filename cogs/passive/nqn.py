"""
Credits: https://github.com/animeforreal
"""
import discord, re

from discord.ext import commands

class NQN(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def find_emoji(self, string):
        emoji = discord.utils.get(self.client.emojis, name = string.strip(":"))
        if emoji is not None:
            if emoji.animated:
                add = ''
            else:
                add = ''
            return f"<{add}:{emoji.name}:{emoji.id}>"
        else:
            return None

    async def get_emoji_name(self, content):
        return_lst = [] #The list that the function will return in the end

        words_of_content = content.split(' ') #List will have n number of items, n being the number of words
        seperate_emoji_name = content.split(':') #List wil have 3 items, content before the emoji name, and content after the emoji name

        if len(seperate_emoji_name) > 1: #This will most likely happen
            for word in words_of_content:
                if word.count(':') > 1: #If there are more than 1 colons in the message
                    temp_var = ''
                    if word.startswith('<') and word.endswith('>'): #The emoji
                        return_lst.append(word)
                    else:
                        seperate_emoji_name = 0
                        for i in word:
                            if seperate_emoji_name == 2:
                                temp_var_2 = temp_var.replace(' ','')
                                return_lst.append(temp_var_2)
                                temp_var = ''
                                seperate_emoji_name = 0

                            if i != ':':
                                temp_var += i
                            else:
                                if temp_var == '' or seperate_emoji_name == 1:
                                    temp_var += ' : '
                                    seperate_emoji_name += 1
                                else:
                                    temp_var_2 = temp_var.replace(' ','')
                                    return_lst.append(temp_var_2)
                                    temp_var = ':'
                                    seperate_emoji_name = 1


                        temp_var_2 = temp_var.replace(' ','') #remove blank spaces
                        return_lst.append(temp_var_2)

                else:
                    return_lst.append(word)
        else:
            return content

        return return_lst

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.bot:
            return

        if ':' in msg.content:
            message = await self.get_emoji_name(msg.content)
            return_string = '' #final message that the bot will send

            needs_nitro = False

            list_ = msg.content.split(':')
            if len(list_) > 1:
                for word in message:
                    if word.startswith(':') and word.endswith(':') and len(word) > 1:
                        emoji = await self.find_emoji(word)

                        if emoji is not None:
                            if not '<a:': #Check if emoji is animated
                                needs_nitro = False #Anyone can send a non-animated emoji from the server.
                                return
                            else:
                                needs_nitro = True
                                return_string += f" {emoji}"

                        else:
                            return_string += f" {word}"

                    else:
                        return_string += f" {word}"
            else:
                ret += message

            if needs_nitro == True:
                await msg.channel.send(return_string)




def setup(client):
    client.add_cog(NQN(client))
    print('NQN')
