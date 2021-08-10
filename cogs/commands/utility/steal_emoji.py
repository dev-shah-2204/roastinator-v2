"""
Got help from
https://blacktooth-bot.com
for this one
"""

import discord
import requests
import shutil

from discord.ext import commands


class StealEmoji(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["stealemoji", "emojiadd"], description="Download emojis that you have access to and upload them to your own server.")
    @commands.has_permissions(manage_emojis=True)
    async def steal(self, ctx, emoji_name, custom_emoji_name=None):
        await self.emoji_from_url(ctx, emoji_name, custom_emoji_name)


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
            await self.install_emoji(ctx=ctx, emoji_json={"title": emoji_name, "image": image_url}, success_message= "E")
        except requests.exceptions.MissingSchema or requests.exceptions.InvalidSchema:
            await ctx.send(f"{image_url}... That doesn't seem like an emoji or an image")


    async def install_emoji(self, ctx, emoji_json, success_message: str = None):
        response = requests.get(emoji_json["image"], stream=True)

        if response.status_code == 200:
            with open(f"./emojis/{emoji_json['title']}.gif", "wb") as img:
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, img)

        else:
            raise Exception(f"Bad status code uploading {emoji_json['title']} received: {response.status_code}")

        with open(f"./emojis/{emoji_json['title']}.gif", "rb") as image:
            try:
                if isinstance(ctx, discord.Guild):
                    new_emoji = await ctx.create_custom_emoji(name=emoji_json['title'], image=image.read())
                else:
                    new_emoji = await ctx.message.guild.create_custom_emoji(name=emoji_json['title'], image=image.read())
            except discord.HTTPException:
                await ctx.send("Only letters, numbers and underscores (_) are allowed in emoji names.")
                return

                if success_message:
                    embed = discord.Embed(
                        title="Emoji added successfully",
                        colour=discord.Color.green(),
                        description=f"`:{emoji_json['title']}:`"
                        )
                    embed.set_thumbnail(url=emoji_json["image"])

                    await ctx.message.channel.send(embed=embed)
            return new_emoji


def setup(client):
    client.add_cog(StealEmoji(client))
    print('StealEmoji')
