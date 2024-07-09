import discord
import os
import logging
import logging.handlers

intents = discord.Intents.default()
intents.message_content = True
intents.members = True #Enable member intent
intents.reactions = True  # Enable reactions intent
client = discord.Client(intents=intents)
bot_version = '1.0'

#######################################################
##Logging 
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
logging.getLogger('discord.http').setLevel(logging.INFO)

handler = logging.handlers.RotatingFileHandler(
    filename='discord.log',
    encoding='utf-8',
    maxBytes=32 * 1024 * 1024,  # 32 MiB
    backupCount=5,  # Rotate through 5 files
)
dt_fmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
handler.setFormatter(formatter)
logger.addHandler(handler)

##Error Log Handler
error_handler = logging.FileHandler('error.log', encoding='utf-8')
error_formatter = logging.Formatter('[{asctime}] {levelname}: {message}', dt_fmt, style='{')
error_handler.setFormatter(error_formatter)
error_logger = logging.getLogger('error_logger')
error_handler.setLevel(logging.ERROR)
error_logger.addHandler(error_handler)

## Helper function to log errors
def log_error(action, member, emoji, error):
    '''Sends errors to the error_logger which is formatted to display in a uniform way'''
    error_msg = f"{action} failed. Emoji: {emoji}, User: {member.name} (ID: {member.id}), Error: {error}"
    error_logger.error(error_msg)

#######################################################
## Event Listeners

## Bot is Ready
@client.event
async def on_ready():
    '''Sends a msg to the console when connected and ready'''
    print(f'We have logged in as {client.user}')

## Message listener
@client.event
async def on_message(message):
    '''Listens for a message then does something based on the message'''
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

## Member join event
@client.event
async def on_member_join(member):
    try:
        channel = discord.utils.get(member.guild.channels, name='member-log')
        await channel.send(f'{member.id} {member.name} has joined the server')
    except AttributeError:
        error_logger.error(f"Channel 'member-log' not found or bot does not have permission to access it.")
    except Exception as e:
        error_logger.error(f"Unexpected error: {e}")

## Member leave event
@client.event
async def on_member_remove(member):
    try:
        channel = discord.utils.get(member.guild.channels, name='member-log')
        await channel.send(f'{member.id} {member.name} has left the server.')
    except AttributeError:
        error_logger.error(f"Channel 'member-log' not found or bot does not have permission to access it.")
    except Exception as e:
        error_logger.error(f"Unexpected error: {e}")


## Reaction role functions
emoji_dict = {
    "ofp": "<:OFP:1259651019525193810>",
    "pint": "<:pint:1259642705072357506>"
}
ofp_emoji = '<:OFP:1259651019525193810>'
pint_emoji = '<:pint:1259642705072357506>'
agree_to_rules_msg_id = 1259639530248732673
about_us_and_rules_channel_id = 1108895281149399121

#Need to add handling if member already is higher 'crusader' role
@client.event
async def on_raw_reaction_add(payload):
    if payload.channel_id == about_us_and_rules_channel_id and payload.message_id == agree_to_rules_msg_id:
        guild = client.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)

        # OFP emoji selected. Assign OFP role
        if str(payload.emoji) == ofp_emoji:
            role = discord.utils.get(guild.roles, name='OFP') 
            try:
                await member.add_roles(role)
                await member.send(f'You have been given the {role.name} role!')
            except discord.errors.Forbidden:
                print(f"Bot doesn't have permission to add roles.")
            try:
                channel = discord.utils.get(member.guild.channels, name='member-log')
                await channel.send(f'Discord ID: {member.id}, Discord Name: {member.name} has been given the role {role}.')
            except AttributeError:
                error_logger.error(f"Channel 'member-log' not found or bot does not have permission to access it.")
            except Exception as e:
                error_logger.error(f"Unexpected error: {e}")

        # pint emoji selected. Assign squires role
        elif str(payload.emoji) == pint_emoji:
            role = discord.utils.get(guild.roles, name='Squires')
            print(role)
            try:
                await member.add_roles(role)
                await member.send(f'You have been given the {role.name} role!')
            except discord.errors.Forbidden:
                print(f"Bot doesn't have permission to add roles.")
            try:
                channel = discord.utils.get(member.guild.channels, name='member-log')
                await channel.send(f'Discord ID: {member.id}, Discord Name: {member.name} has been given the role {role}.')
            except AttributeError:
                error_logger.error(f"Channel 'member-log' not found or bot does not have permission to access it.")
            except Exception as e:
                error_logger.error(f"Unexpected error: {e}")

client.run(os.getenv('TOKEN'))