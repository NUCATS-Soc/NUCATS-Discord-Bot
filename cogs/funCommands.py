import discord
from discord.ext import commands
import aiohttp
import random


class FunCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["random", "randomnumber", "randomNumber", "rand", "randnum", "randNum"])
    async def ran(self, ctx, arg1, arg2):
        await ctx.channel.send("🎲 Your random number is : " + str(random.randint(int(arg1), int(arg2))))

    @commands.command(aliases=["flipcoin", "flipCoin", "coin", "Coin"])
    async def flip(self, ctx):
        await ctx.channel.send(f"{ctx.message.author.mention}🪙 throws a coin in the air and it lands on....")
        if random.randint(0, 2) == 1:
            await ctx.channel.send("HEADS")
        else:
            await ctx.channel.send("TAILS")

    @commands.command(aliases=["dog", "dogs", "nudogs"])
    async def nudog(self, ctx):
        async with aiohttp.ClientSession() as session:
            request = await session.get("https://some-random-api.ml/img/dog")
            dogjson = await request.json()
        embed = discord.Embed(title="OMG! A doggo! 🐶", color=discord.Color.purple())
        embed.set_image(url=dogjson["link"])
        await ctx.send(embed=embed)

    @commands.command(aliases=["cat", "cats", "nucats"])
    async def nucat(self, ctx):
        async with aiohttp.ClientSession() as session:
            request = await session.get("https://some-random-api.ml/img/cat")
            dogjson = await request.json()
        embed = discord.Embed(title="I was made to code this...", color=discord.Color.purple())
        embed.set_image(url=dogjson["link"])
        await ctx.send(embed=embed)


async def setup(client):
    await client.add_cog(FunCommands(client))
