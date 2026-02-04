import discord
from discord import app_commands

FEATURE = {
    "slug": "say_copy",
    "name": "Say Feature",
    "description": "A feature that allows the bot to say messages.",
    "version": "1.0.0",
    "author": "Tryno",
    "requires_config": True,
    "permissions": ["send_messages", "embed_links"]
}

def register(tree : app_commands.CommandTree, config):
    @tree.command(name="say", description=FEATURE["description"])
    @app_commands.describe(message="The message for the bot to say.")
    async def say_command(interaction: discord.Interaction, message: str):
        ephemeral_default = bool(config.get("ephemeral_default")) if isinstance(config, dict) else False
        await interaction.response.send_message(message, ephemeral=ephemeral_default)