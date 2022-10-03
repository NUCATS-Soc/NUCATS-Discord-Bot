from discord.ext import commands

import ids
import tools


class CommitteePoints(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def points(self, ctx, name):
        if ctx.channel.id not in ids.committee_group:
            return

        name = name.lower()
        if name in ["all", "*"]:
            results = await tools.querySelect(f"""SELECT * FROM committee_points;""")
            await ctx.channel.send("**Committee Points:**")
            for item in results:
                await ctx.channel.send(f"{item[0]} - {item[1]}".capitalize())
        else:
            results = await tools.querySelect(f"""SELECT * FROM committee_points WHERE id = "{name}";""")
            await ctx.channel.send(f"{results[0][0]} has {results[0][1]} points".capitalize())

    @commands.command()
    async def add_points(self, ctx, name, value):
        if ctx.channel.id not in ids.committee_group:
            return

        name = name.lower()
        points = await tools.querySelect(f"""SELECT * FROM committee_points WHERE id = "{name}";""")
        points2 = points[0][1] + int(value)
        await tools.queryInsert(f"""UPDATE committee_points SET points = {points2} WHERE id = "{name}";""")
        await ctx.channel.send(f"Added {value} points to {name.capitalize}!")

    @commands.command()
    async def add_user(self, ctx, name):
        if ctx.channel.id not in ids.committee_group:
            return

        name = name.lower()
        await tools.queryInsert(f"""INSERT INTO committee_points(id,points) VALUES("{name}", 0)""")
        await ctx.channel.send(f"Added {name.capitalize()}")


async def setup(client):
    await client.add_cog(CommitteePoints(client))
