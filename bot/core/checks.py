from __future__ import annotations

from typing import Callable, List, Union
from functools import wraps

import discord
from discord import app_commands

# global check decorators for features
# import with: from bot.core.checks import is_staff, is_server_admin, ...

_staff_roles_ids: List[int] = []

def set_staff_roles(roles_ids: List[int]) -> None:
    """set staff roles ids from env config"""
    global _staff_roles_ids
    _staff_roles_ids = roles_ids

def _extract_id(obj: Union[int, discord.Role, discord.Member, discord.User, discord.abc.Snowflake]) -> int:
    """extract id from discord obj or return int directly"""
    if isinstance(obj, int):
        return obj
    return obj.id

def _extract_ids(objs: tuple) -> List[int]:
    """extract ids from multiple discord objs or ints"""
    return [_extract_id(obj) for obj in objs]

def _has_any_role(member: discord.Member, role_ids: List[int]) -> bool:
    """check if member has any of the specified roles"""
    return any(role.id in role_ids for role in member.roles)

# --- check decorators ---

def is_staff() -> Callable:
    """check if user has a staff role (defined in env STAFF_ROLES_IDS)"""
    async def predicate(interaction: discord.Interaction) -> bool:
        if not isinstance(interaction.user, discord.Member):
            return False
        if not _staff_roles_ids:
            return False
        return _has_any_role(interaction.user, _staff_roles_ids)
    return app_commands.check(predicate)

def is_server_admin() -> Callable:
    """check if user has admin permissions"""
    async def predicate(interaction: discord.Interaction) -> bool:
        if not isinstance(interaction.user, discord.Member):
            return False
        return interaction.user.guild_permissions.administrator
    return app_commands.check(predicate)

def is_server_owner() -> Callable:
    """check if user is server owner"""
    async def predicate(interaction: discord.Interaction) -> bool:
        if not interaction.guild:
            return False
        return interaction.user.id == interaction.guild.owner_id
    return app_commands.check(predicate)

def is_server_mod() -> Callable:
    """check if user has mod perms (manage messages, kick, ban)"""
    async def predicate(interaction: discord.Interaction) -> bool:
        if not isinstance(interaction.user, discord.Member):
            return False
        perms = interaction.user.guild_permissions
        return perms.manage_messages or perms.kick_members or perms.ban_members
    return app_commands.check(predicate)

def has_permissions(**perms) -> Callable:
    """check if user has specific permissions"""
    async def predicate(interaction: discord.Interaction) -> bool:
        if not isinstance(interaction.user, discord.Member):
            return False
        user_perms = interaction.user.guild_permissions
        return all(getattr(user_perms, perm, False) for perm in perms if perms[perm])
    return app_commands.check(predicate)

def has_any_role(*roles: Union[int, discord.Role]) -> Callable:
    """check if user has any of the specified roles (ids or Role objs)"""
    async def predicate(interaction: discord.Interaction) -> bool:
        if not isinstance(interaction.user, discord.Member):
            return False
        return _has_any_role(interaction.user, _extract_ids(roles))
    return app_commands.check(predicate)

def has_all_roles(*roles: Union[int, discord.Role]) -> Callable:
    """check if user has all the specified roles (ids or Role objs)"""
    async def predicate(interaction: discord.Interaction) -> bool:
        if not isinstance(interaction.user, discord.Member):
            return False
        member_role_ids = {role.id for role in interaction.user.roles}
        required_ids = _extract_ids(roles)
        return all(rid in member_role_ids for rid in required_ids)
    return app_commands.check(predicate)

def in_channel(*channels: Union[int, discord.abc.GuildChannel]) -> Callable:
    """check if cmd is used in specific channels (ids or Channel objs)"""
    async def predicate(interaction: discord.Interaction) -> bool:
        return interaction.channel_id in _extract_ids(channels)
    return app_commands.check(predicate)

def in_category(*categories: Union[int, discord.CategoryChannel]) -> Callable:
    """check if cmd is used in specific category (ids or Category objs)"""
    async def predicate(interaction: discord.Interaction) -> bool:
        if not interaction.channel or not hasattr(interaction.channel, 'category_id'):
            return False
        return interaction.channel.category_id in _extract_ids(categories)
    return app_commands.check(predicate)

def is_nsfw() -> Callable:
    """check if channel is nsfw"""
    async def predicate(interaction: discord.Interaction) -> bool:
        if not interaction.channel:
            return False
        return getattr(interaction.channel, 'nsfw', False)
    return app_commands.check(predicate)

def bot_has_permissions(**perms) -> Callable:
    """check if bot has specific permissions in channel"""
    async def predicate(interaction: discord.Interaction) -> bool:
        if not interaction.guild or not interaction.channel:
            return False
        bot_member = interaction.guild.me
        if not bot_member:
            return False
        channel_perms = interaction.channel.permissions_for(bot_member)
        return all(getattr(channel_perms, perm, False) for perm in perms if perms[perm])
    return app_commands.check(predicate)

def cooldown(rate: int, per: float, *, key: Callable = None) -> Callable:
    """apply cooldown to cmd (wrapper for app_commands.checks.cooldown)"""
    return app_commands.checks.cooldown(rate, per, key=key)
