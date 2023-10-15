from typing import TYPE_CHECKING

from discord.ext import commands

from tools import log

if TYPE_CHECKING:
    from discord.client import Bot


class OnStart(commands.Cog):
    def __init__(self, client: "Bot"):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        await log(self.client, "**Bot is online**")


async def setup(client: "Bot"):
    await client.add_cog(OnStart(client))
