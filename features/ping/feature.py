import discord
from discord import app_commands

FEATURE = {
    "slug": "ping",
    "name": "Ping Feature",
    "description": "A feature that responds to ping commands.",
    "version": "1.0.0",
    "author": "Tryno",
    "requires_config": False,
    "permissions": ["send_messages", "embed_links"]
}

def register(tree, config):
    @tree.command(name="ping", description="Responds with Pong!")
    async def ping_command(interaction: discord.Interaction):
        await interaction.response.send_message("Pong!")