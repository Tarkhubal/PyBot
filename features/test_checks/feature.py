import discord
from discord import app_commands
from bot.core.checks import (
    is_staff,
    is_server_admin,
    is_server_owner,
    is_server_mod,
    has_permissions,
    cooldown
)

FEATURE = {
    "slug": "test_checks",
    "name": "Test Checks Feature",
    "description": "Feature to test global checks decorators.",
    "version": "1.0.0",
    "author": "Thomas",
    "requires_config": False,
    "permissions": ["send_messages"]
}

def register(tree: app_commands.CommandTree, config):
    group = app_commands.Group(name="checktest", description="Test checks decorators")

    @group.command(name="admin", description="Test is_server_admin check")
    @is_server_admin()
    async def test_admin(interaction: discord.Interaction):
        await interaction.response.send_message("✅ Tu es admin !", ephemeral=True)

    @group.command(name="owner", description="Test is_server_owner check")
    @is_server_owner()
    async def test_owner(interaction: discord.Interaction):
        await interaction.response.send_message("✅ Tu es le propriétaire !", ephemeral=True)

    @group.command(name="mod", description="Test is_server_mod check")
    @is_server_mod()
    async def test_mod(interaction: discord.Interaction):
        await interaction.response.send_message("✅ Tu es modérateur !", ephemeral=True)

    @group.command(name="staff", description="Test is_staff check")
    @is_staff()
    async def test_staff(interaction: discord.Interaction):
        await interaction.response.send_message("✅ Tu es staff !", ephemeral=True)

    @group.command(name="manage_messages", description="Test has_permissions check")
    @has_permissions(manage_messages=True)
    async def test_manage_messages(interaction: discord.Interaction):
        await interaction.response.send_message("✅ Tu peux gérer les messages !", ephemeral=True)

    @group.command(name="cooldown", description="Test cooldown check (1 use per 10s)")
    @cooldown(1, 10.0)
    async def test_cooldown(interaction: discord.Interaction):
        await interaction.response.send_message("✅ Cooldown passé !", ephemeral=True)

    @group.command(name="info", description="Show your permissions info")
    async def test_info(interaction: discord.Interaction):
        if not isinstance(interaction.user, discord.Member):
            await interaction.response.send_message("❌ Commande serveur uniquement", ephemeral=True)
            return
        
        perms = interaction.user.guild_permissions
        roles = [r.name for r in interaction.user.roles if r.name != "@everyone"]
        
        embed = discord.Embed(title="Tes informations", color=discord.Color.blurple())
        embed.add_field(name="Admin", value="✅" if perms.administrator else "❌", inline=True)
        embed.add_field(name="Propriétaire", value="✅" if interaction.user.id == interaction.guild.owner_id else "❌", inline=True)
        embed.add_field(name="Mod", value="✅" if (perms.manage_messages or perms.kick_members or perms.ban_members) else "❌", inline=True)
        embed.add_field(name="Rôles", value=", ".join(roles) if roles else "Aucun", inline=False)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

    tree.add_command(group)
