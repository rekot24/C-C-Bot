import discord
from main import log_error


emoji_dict = {
    "ofp": "<:OFP:1259651019525193810>",
    "pint": "<:pint:1259642705072357506>"
}

async def handle_role(guild, member, role_name, action):
    role = discord.utils.get(guild.roles, name=role_name)
    if not role:
        log_error("Fetching role", member, None, f"Role {role_name} not found.")
        return

    try:
        if action == "add":
            await member.add_roles(role)
            await member.send(f'You have been given the {role.name} role!')
        elif action == "remove":
            await member.remove_roles(role)
            await member.send(f'The {role.name} role has been removed.')
    except discord.errors.Forbidden:
        log_error(f"{action.capitalize()}ing role", member, None, "Bot doesn't have permission to modify roles.")
    except Exception as e:
        log_error(f"{action.capitalize()}ing role", member, None, str(e))

    try:
        channel = discord.utils.get(member.guild.channels, name='member-log')
        if action == "add":
            await channel.send(f'{member.id} {member.name} has been given the role {role.name}.')
        elif action == "remove":
            await channel.send(f'{member.id} {member.name} has had the role {role.name} removed.')
    except AttributeError:
        log_error(f"Sending {action} role message", member, None, "Channel 'member-log' not found or bot does not have permission to access it.")
    except Exception as e:
        log_error(f"Sending {action} role message", member, None, str(e))
