import requests
from discord.ext import commands
import tools


class CommitteePoints(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def points(self, ctx, name):
        results = await tools.querySelect(f"""SELECT * FROM committee_points WHERE id = "{arg1}";""")
        await ctx.channel.send(f"{results[0][0]} has {results[0][1]} points")

    @commands.command()
    async def add_points(self, ctx, name, value):
        points = await tools.querySelect(f"""SELECT * FROM committee_points WHERE id = "{name}";""")
        points2 = points[0][1] + int(value)
        await tools.queryInsert(f"""UPDATE committee_points SET points = {points2} WHERE id = "{name}";""")

    @commands.command()
    async def add_user(self, ctx, name):
        await tools.queryInsert(f"""INSERT INTO committee_points(id,points) VALUES("{name}", 0)""")


async def setup(client):
    await client.add_cog(CommitteePoints(client))
