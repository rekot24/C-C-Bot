import discord
import os
import logging
import logging.handlers

intents = discord.Intents.default()
intents.message_content = True
intents.members = True #Enable member intent
intents.reactions = True  # Enable reactions intent
client = discord.Client(intents=intents)

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

#Error Logger
error_handler = logging.FileHandler('error.log', encoding='utf-8')
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(formatter)
logger.addHandler(error_handler)

#######################################################
## Event Listeners

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

# Member join event
@client.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.channels, name='member-log')  # Replace 'general' with your desired channel
    if channel:
        await channel.send(f'Welcome {member.mention} to the server!')

# Member leave event
@client.event
async def on_member_remove(member):
    channel = discord.utils.get(member.guild.channels, name='member-log')  # Replace 'general' with your desired channel
    if channel:
        await channel.send(f'{member.mention} has left the server.')

# Reaction role assignment
@client.event
async def on_raw_reaction_add(payload):
    if payload.channel_id == 1108895281149399121:  #about-us-and-rules channel ID
        guild = client.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)

        # OFP emoji selected. Assign OFP role
        if str(payload.emoji) == '<:OFP:1259651019525193810>':
            role = discord.utils.get(guild.roles, name='OFP') 
            if role:
                try:
                    await member.add_roles(role)
                    await member.send(f'You have been given the {role.name} role!')
                except discord.errors.Forbidden:
                    print(f"Bot doesn't have permission to add roles.")

        # pint emoji selected. Assign squires role
        elif str(payload.emoji) == '<:pint:1259642705072357506>':
            role = discord.utils.get(guild.roles, name='Squires')
            if role:
                try:
                    await member.add_roles(role)
                    await member.send(f'You have been given the {role.name} role!')
                    print("role selected")
                except discord.errors.Forbidden:
                    print(f"Bot doesn't have permission to add roles.")

client.run(os.getenv('TOKEN'))