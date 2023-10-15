import asyncio
import os

import discord
from discord.ext import commands

# Gets application token
with open("token.txt", encoding="utf-8") as file:
    token = file.read()

intents = discord.Intents.all()
client = commands.Bot(command_prefix="!", intents=intents)


async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")


# Loads all cogs then starts the bot
async def main():
    await load()
    await client.start(token)


asyncio.run(main())
