import discord
from discord import app_commands

FEATURE = {
    "slug": "ping", # The unique identifier for the feature
    "name": "Ping Feature", # The display name of the feature
    "description": "A feature that responds to ping commands.", # A brief description of the feature
    "version": "1.0.0", # The version of the feature
    "author": "Tryno", # The author of the feature
    "requires_config": False, # Whether the feature requires configuration
    "permissions": ["send_messages", "embed_links"] # Required permissions
}

def register(tree, config): # Register the feature's commands with the bot's command tree
    @tree.command(name=FEATURE["slug"], description=FEATURE["description"]) # Define a new command in the command tree
    @app_commands.describe() # No parameters to describe for this command
    async def ping_command(interaction: discord.Interaction): # The command function that will be called when the command is invoked
        await interaction.response.send_message("Pong!") # Respond with "Pong!" when the command is used
        # Add any additional logic for your custom feature here