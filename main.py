import asyncio
import os

import discord
from discord.ext import commands

from config import Config


async def load(client: "commands.Bot"):
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")


# Loads all cogs then starts the bot
async def main():
    intents = discord.Intents.all()
    client = commands.Bot(command_prefix="!", intents=intents)
    await load(client)
    await client.start(Config.get("TOKEN"))


if __name__ == "__main__":
    asyncio.run(main())
