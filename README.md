[![Discord Bots](https://top.gg/api/widget/status/822795444089782293.svg)](https://top.gg/bot/822795444089782293) [![Discord Bots](https://top.gg/api/widget/servers/822795444089782293.svg)](https://top.gg/bot/822795444089782293)
# Utility/Moderation Discord Bot

I'm assuming you know basic python before viewing this code. If not, you are going to have a hard time customizing it. I have put comments all over the code to help you understand it, but I wouldn't be so sure about the ease of customizing the bot.

Refer LICENSE for copyright details. *Spoiler Alert*: You can do anything you like with this code. Heck even copy it all and say it's your own and I can't say anything.

## Why each command code is in a separate file
Modularity and customizability. For beginners making their personal discord bot, removing commands becomes an easier job. Also, when testing multiple features at the same time, you don't need to comment things out, as you can choose to not load the cog/extension for a particular test.

## YouTube
There are tons of YouTube videos that show in detail how to make your own Discord Bot using python. If you have difficulty understanding how to make a bot here, well, this isn't a tutorial. This is code for you to copy and paste to add features to your bot without spending a lot of time. Check out [Carberra Tutorials](https://www.youtube.com/channel/UC13cYu7lec-oOcqQf5L-brg) and [Menu Docs](https://www.youtube.com/channel/UCpGGFqJP9vYvzFudqnQ-6IA). They have a great series of tutorials on a python discord bot.</br>
If you wish to learn python, [this](https://youtu.be/_uQrJ0TkZlc) tutorial from [Programming with Mosh](https://youtu.be/_uQrJ0TkZlc) is really nice.

## Other open-sourced bots
[Carl-Bot](https://github.com/CarlGroth/Carl-Bot) - Has great features. It is made in python. \[Outdated\]<br />
[YAGPDP](https://github.com/jonas747/yagpdb) - Also has great features. It's not made in python.


## Some important pointers:
• For understanding how cogs work, refer to the first cog i.e. `cogs/events/modmail` <br />
• For understanding how to take input after a command is run, refer to the first game cog i.e. `cogs/commands/games/cointoss`
• If you're making commands that use a database, make sure that the operation statement is correct according to your table
• Hosting the bot isn't a difficult, heroku is fine for a bot of this level.
