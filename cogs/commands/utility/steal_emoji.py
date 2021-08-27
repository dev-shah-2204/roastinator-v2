"""
Got help from
https://blacktooth-bot.com
for this one
"""

import discord
import requests
import shutil
import hex_colors

from discord.ext import commands


class StealEmoji(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["stealemoji", "emojiadd"], description="Download emojis that you have access to and upload them to your own server.")
    @commands.has_permissions(manage_emojis=True)
    async def steal(self, ctx, emoji, custom_emoji_name=None):
        if "tenor.com" in emoji or "https://tenor.com" in emoji:
            await ctx.send("You can't steal emojis from tenor links (yet)")
            return

        await self.emoji_from_url(ctx, emoji, custom_emoji_name)


    async def emoji_from_url(self, ctx, emoji_name, custom_emoji_name=None, image=None):
        if image is None:
            if len(ctx.message.attachments) == 0:
                image = emoji_name
                emoji_name = None

        image_url = None
        if image:
            try:
                image = await discord.ext.commands.PartialEmojiConverter.convert(self, ctx=ctx, argument=image)

                if custom_emoji_name is not None:
                    emoji_name = custom_emoji_name
                else:
                    emoji_name = image.name

                image_url = image.url

            except commands.BadArgument:
                image_url = image

        elif len(ctx.message.attachments) > 0:
            image_url = ctx.message.attachments[0].url

        try:
            await self.install_emoji(ctx=ctx, emoji_json={"title": custom_emoji_name, "image": image_url})
        except requests.exceptions.MissingSchema:
            await ctx.send(f"{image_url}... That doesn't seem like an emoji or an image")


    async def install_emoji(self, ctx, emoji_json):
        response = requests.get(emoji_json["image"], stream=True)

        set_footer = False
        title = emoji_json['title']

        if title is None:
            title = 'some_emoji'
            set_footer = True

        if response.status_code == 200:

            with open(f"./emojis/{title}.gif", "wb") as img:
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, img)

        else:
            raise Exception(f"Bad status code uploading {title} received: {response.status_code}")

        with open(f"./emojis/{title}.gif", "rb") as image:
            try:
                if isinstance(ctx, discord.Guild):
                    new_emoji = await ctx.create_custom_emoji(name=title, image=image.read())
                else:
                    new_emoji = await ctx.message.guild.create_custom_emoji(name=title, image=image.read())

            except discord.InvalidArgument:
                try:
                    response = requests.get(emoji_json['image'])
                    new_image = open("./emojis/some_emoji.gif", "wb")
                    new_image.write(response.content)
                    new_image.close()

                    with open(f"./emojis/some_emoji.gif", "rb") as img:
                        if isinstance(ctx, discord.Guild):
                            new_emoji = await ctx.create_custom_emoji(name=title, image=img.read())
                        else:
                            new_emoji = await ctx.message.guild.create_custom_emoji(name=title, image=img.read())

                except:
                    await ctx.send("An error occured when retrieving the image from the given emoji/URL")

            except discord.HTTPException as e:
                if e.code == 400:
                    await ctx.send("Only letters, numbers and underscores are allowed in emoji names.")
                    return

            embed = discord.Embed(
                title="Emoji added successfully",
                colour=hex_colors.l_green,
                description=f"`:{title}:`"
                )
            embed.set_thumbnail(url=emoji_json["image"])

            if set_footer:
                embed.set_footer(text="Sorry for the trouble, but you'll have to rename the emoji.")

            await ctx.message.channel.send(embed=embed)


def setup(client):
    client.add_cog(StealEmoji(client))
    print('StealEmoji')
