import discord
from discord import app_commands

FEATURE = {
    "slug": "version", 
    "name": "Version Feature", 
    "description": "A feature that provides the bot's version information.", 
    "version": "1.0.0",
    "author": "Tryno", 
    "requires_config": False,
    "permissions": ["send_messages", "embed_links"]   
}

def register(tree : app_commands.CommandTree, config): 
    @tree.command(name=FEATURE["slug"], description=FEATURE["description"]) 
    async def version_command(interaction: discord.Interaction): 
        """
        Provide the bot's version information.
        Arguments:
            interaction: The interaction object.
        """
        bot_version = FEATURE["version"]
        embed = discord.Embed(
            title="Bot Version",
            description=f"The current bot version is {bot_version}.",
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)