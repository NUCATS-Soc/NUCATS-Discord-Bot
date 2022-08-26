from discord.ext import commands

from tools import log


class OnStart(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        await log(self.client, "**Bot is online**")
        print("Bot is online")


async def setup(client):
    await client.add_cog(OnStart(client))
