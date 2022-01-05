# Roastinator

Roastinator is supposed to be a utility and moderation discord bot. I've tried my best to keep the bot as customisable as possible so that you can run an instance of it yourself. Refer `LICENSE` for copyright details. *Spoiler Alert*: You can copy any and everything except sensitive details like API keys (which are kept as environment tables for obvious reasons). Want to run your own Roastinator? Sure go ahead. I'd appreciate if you'd mention my name or the link to this repository in the start of your code or in your README.

## Config Vars

**Database**:<br>
db_host     - The host URL of your database (Might be your IPv4 or localhost)<br>
db_user     - The username (root in most cases)<br>
db_password - The password (Leave it as `""` if it's not password protected)<br>
db_db       - The name of the database

**API Keys**:<br>
dad_key_1      - Key for the dad joke api (get from rapid-api)<br>
urban_dict_key - Key for the urban dictionary api (get from rapid-api)<br>
STEAM_API_KEY  - Key for the Steam API (get from steam)

**Bot Related**<br>
discord_id      - Your discord ID (The owner ID)<br>
token           - The bot token<br>
error_channel   - The channel where you want to receive errors<br>
modmail_channel - The channel where you want to receive mod mail<br>


## Database (MySQL)
- Auto Mod setup:<br>
```
CREATE TABLE automod(
    guild VARCHAR(20) PRIMARY KEY,
    _status VARCHAR(10)
)
```

- Command Blacklist setup:<br>
```
CREATE TABLE command_blacklist(
    user_id VARCHAR(20) PRIMARY KEY
)
```

- Modmail Ban setup:<br>
```
CREATE TABLE modban(
    user_id VARCHAR(20) PRIMARY KEY
)
```

- Prefix setup:<br>
```
CREATE TABLE prefix(
    guild VARCHAR(20) PRIMARY KEY,
    prefix VARCHAR(5)
)
```

## NOTE

This is not a tutorial on how to make a discord bot.
