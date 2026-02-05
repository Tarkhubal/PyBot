from __future__ import annotations

import logging
import os
from datetime import date
from logging.handlers import RotatingFileHandler
from pathlib import Path

import discord
from discord.ext import commands
from dotenv import load_dotenv

from ..core.checks import set_staff_roles
from ..core.config import load_config, load_env
from ..core.loader import load_features


def setup_logging(level: str = "INFO") -> None:
    logs_dir = Path(__file__).resolve().parent.parent.parent / "logs"
    logs_dir.mkdir(exist_ok=True)

    fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")

    root = logging.getLogger()
    root.setLevel(getattr(logging, level.upper(), logging.INFO))
    root.handlers.clear()

    sh = logging.StreamHandler()
    sh.setFormatter(fmt)
    root.addHandler(sh)

    fh = RotatingFileHandler(
        logs_dir / f"bot_{date.today().isoformat()}.log",
        maxBytes=5_000_000,
        encoding="utf-8",
    )
    fh.setFormatter(fmt)
    root.addHandler(fh)


class BotApp(commands.Bot):
    def __init__(self, guild_id: int) -> None:
        intents = discord.Intents.default()
        super().__init__(command_prefix="!", intents=intents)
        self.guild = discord.Object(id=guild_id)

    async def setup_hook(self) -> None:
        self.tree.clear_commands(guild=None)
        await self.tree.sync()

        loaded, failed = load_features(self.tree, self.config)
        logging.getLogger(__name__).info(f"Loaded features: {list(loaded.keys())}")
        if failed:
            logging.getLogger(__name__).warning(f"Failed to load features: {failed}")

        self.tree.copy_global_to(guild=self.guild)
        synced = await self.tree.sync(guild=self.guild)
        logging.getLogger(__name__).info("Synced %d commands to guild %s", len(synced), self.guild.id)


def main() -> None:
    setup_logging(level=os.getenv("LOG_LEVEL", "INFO"))
    load_dotenv()
    env = load_env()
    set_staff_roles(env.staff_roles_ids)

    config = load_config(env.config_path)

    bot = BotApp(guild_id=env.guild_id)
    bot.config = config

    bot.run(env.discord_token)


if __name__ == "__main__":
    main()
