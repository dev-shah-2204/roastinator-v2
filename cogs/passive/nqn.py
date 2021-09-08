import discord

from discord.ext import commands


class NQN(commands.Cog):
    """
    The code can get a little confusing, I couldn't write it better than this.
    The message is first checked for colons. If there are more than 1 colon.
    If yes, then it loops through each word of the message to find potential emojis.
    If any word in this structure is found - <anything> - then it splits that word between the colons.
    Then using discord.utils, the bot checks if an emoji with that name (the name found in the previous step) exists.
    If yes, then the message is deleted and using webhooks, is resent.
    """
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, msg):
        author = msg.author  # For ease of access
        channel = msg.channel  # For ease of access
        message = msg.content  # For ease of access
        guild = msg.guild  # For ease of access

        if not author.bot:
            if ":" in message and message.count(":") > 1:
                nqn = False  # Whether or not it is required to call this event
                sentence_cln = message.split(":")  # List of all the string separated by a colon or ":"
                sentence_spc = message.split(" ")  # List of all the words in the message

                for word in sentence_spc:
                    print(word)
                    if word.startswith("<") and word.endswith(">"):
                        print('condition met')
                        emoji_str = word.split(":")
                        emoji = discord.utils.get(guild.emojis, name=emoji_str[1])
                        print(emoji_str[1])

                        if emoji:
                            print(emoji)
                            print('found emoji')

                            if emoji.animated:
                                nqn = True
                                message = message.replace(word, f"<a:{emoji.name}:{emoji.id}>")
                            else:
                                nqn = False

                    else:  # If emoji was not properly separated from the rest of the words
                        found_potential_emoji = False
                        for char in word:  # each character
                            if char == "<":
                                word = word[word.index(char):]
                                for _char in word:
                                    if char == ">":
                                        word = word[word.index(char):]
                                        found_potential_emoji = True

                        if found_potential_emoji:
                            emoji_str = word.split(":")
                            emoji = discord.utils.get(guild.emojis, name=emoji_str[1])

                            if emoji:
                                if emoji.animated:
                                    nqn = True
                                    message = message.replace(word, f"<a:{emoji.name}:{emoji.id}>")
                                else:
                                    nqn = False

                if nqn:
                    if guild.me.guild_permissions.manage_messages and guild.me.guild_permissions.manage_webhooks:
                        webhooks = await channel.webhooks()
                        webhook = discord.utils.get(webhooks, name='roastinator')

                        if webhook is None:
                            webhook = await channel.create_webhook(name='roastinator')

                        await webhook.send(message,
                                           username=author.display_name,
                                           avatar_url=author.avatar_url,
                                           allowed_mentions=discord.AllowedMentions(everyone=False, roles=False)
                                           )
                        await msg.delete()


def setup(client):
    client.add_cog(NQN(client))
    print("NQN")
