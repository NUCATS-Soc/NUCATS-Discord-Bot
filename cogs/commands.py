import discord
from discord.ext import commands
import aiohttp
import random

import ids
import tools


class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["random", "randomnumber", "rand", "randnum"])
    async def ran(self, ctx, arg1, arg2):
        await ctx.channel.send("🎲 Your random number is : " + str(random.randint(int(arg1), int(arg2))))

    @commands.command(aliases=["flipcoin", "coin"])
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

    @commands.command()
    async def joke(self, ctx):
        async with aiohttp.ClientSession() as session:
            request = await session.get("https://some-random-api.ml/joke")
            jokejson = await request.json()
        embed = discord.Embed(title=jokejson["joke"], colour=discord.Color.random())
        await ctx.send(embed=embed)

    @commands.command(aliases=["pronoun"])
    async def pronouns(self, ctx):
        reaction, user = await tools.get_user_pronouns(self.client, ctx)

        he_him_role = discord.utils.get(self.client.get_guild(ids.server_id).roles, id=ids.he_him_role)
        she_her_role = discord.utils.get(self.client.get_guild(ids.server_id).roles, id=ids.she_her_role)
        they_them_role = discord.utils.get(self.client.get_guild(ids.server_id).roles, id=ids.they_them_role)

        member = self.client.get_guild(ids.server_id).get_member(user.id)

        if str(reaction) == "♂":
            await member.remove_roles(she_her_role)
            await member.remove_roles(they_them_role)
            await member.add_roles(he_him_role)
            pronouns = "He/him"

        elif str(reaction) == "♀":
            await member.remove_roles(he_him_role)
            await member.remove_roles(they_them_role)
            await member.add_roles(she_her_role)
            pronouns = "She/her"

        else:
            await member.remove_roles(she_her_role)
            await member.remove_roles(he_him_role)
            await member.add_roles(they_them_role)
            pronouns = "They/them"

        await tools.log(self.client, f"``{user}`` changed their pronouns to ``{pronouns}``")


async def setup(client):
    await client.add_cog(Commands(client))
