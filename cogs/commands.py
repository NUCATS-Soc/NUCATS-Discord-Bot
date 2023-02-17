import csv

import discord
from discord.ext import commands
import aiohttp
import random

import ids
import tools


class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["random", "randomnumber", "rand", "randnum"], brief="Generates a random number",
                      description="Generates a random number between two given arguments.")
    async def ran(self, ctx, number1, number2):
        await ctx.channel.send("🎲 Your random number is : " + str(random.randint(int(number1), int(number2))))

    @commands.command(aliases=["flipcoin", "coin"], brief="Flips a coin", description="Flips a coin")
    async def flip(self, ctx):
        await ctx.channel.send(f"{ctx.message.author.mention}🪙 throws a coin in the air and it lands on....")
        if random.randint(0, 2) == 1:
            await ctx.channel.send("HEADS")
        else:
            await ctx.channel.send("TAILS")

    @commands.command(aliases=["dog", "dogs", "nudogs"], brief="Gets an image of a dog",
                      description="Gets a random image of a dog")
    async def nudog(self, ctx):
        async with aiohttp.ClientSession() as session:
            request = await session.get("https://some-random-api.ml/img/dog")
            dogjson = await request.json()
        embed = discord.Embed(title="OMG! A doggo! 🐶", color=discord.Color.purple())
        embed.set_image(url=dogjson["link"])
        await ctx.send(embed=embed)

    @commands.command(aliases=["cat", "cats", "nucats"], brief="Gets an image of a cat",
                      description="Gets a random image of a cat")
    async def nucat(self, ctx):
        async with aiohttp.ClientSession() as session:
            request = await session.get("https://some-random-api.ml/img/cat")
            dogjson = await request.json()
        embed = discord.Embed(title="I was made to code this...", color=discord.Color.purple())
        embed.set_image(url=dogjson["link"])
        await ctx.send(embed=embed)

    @commands.command(brief="Tells a joke", description="Tells a joke")
    async def joke(self, ctx):
        async with aiohttp.ClientSession() as session:
            request = await session.get("https://some-random-api.ml/joke")
            jokejson = await request.json()
        embed = discord.Embed(title=jokejson["joke"], colour=discord.Color.random())
        await ctx.send(embed=embed)

    @commands.command(aliases=["rule"], brief="Outputs the server rules", description="Outputs the server rules")
    async def rules(self, ctx):
        with open("rules.txt") as f:
            lines = f.read()
        await ctx.send(lines)

    @commands.command(aliases=["pronoun"], brief="Changes pronouns", description="Updates a users pronoun roles")
    @commands.dm_only()
    async def pronouns(self, ctx):
        reaction, user = await tools.get_user_pronouns(self.client, ctx)

        # Gets roles
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

        await ctx.author.send(f"Your pronouns have been changed to {pronouns}.")
        await tools.log(self.client, f"``{user}`` changed their pronouns to ``{pronouns}``")

    @commands.command(brief="Shows all verified users", description="Shows all verified users and their discord ids")
    @commands.has_role(ids.committee_role)
    @commands.guild_only()
    async def get_verified(self, ctx):
        if ctx.channel.id not in ids.committee_group:
            return

        server = ctx.message.guild

        await ctx.send("**Verified members**")
        for member in server.members:
            for role in member.roles:
                if role.id == ids.verified_role:
                    await ctx.send(f"   display_name: {member.display_name}\n"
                                   f"   id: {member.id}")

    @commands.command(brief="Assigns the member role",
                      description="Gives all paying members who have validate the member role")
    @commands.has_role(ids.committee_role)
    @commands.guild_only()
    async def give_member(self, ctx):
        if ctx.channel.id not in ids.committee_group:
            return

        with open("logs/verified_users.csv", newline="") as file:
            reader = csv.reader(file)
            verified_users = dict(reader)

        with open("logs/members.txt") as file:
            members = file.read().split("\n")

        member_role = discord.utils.get(self.client.get_guild(ids.server_id).roles, id=ids.member_role)

        i = 0
        for member in ctx.message.guild.members:
            for role in member.roles:
                if role.id == ids.verified_role:

                    # Checks the member is verified
                    if str(member.id) not in verified_users.keys():
                        break

                    student_number = verified_users.get(str(member.id))
                    for student in members:
                        if str(student) == str(student_number):
                            i = i + 1
                            await member.add_roles(member_role)
                            await tools.log(self.client,
                                            f"``{member.display_name}`` has been given the **member** role")

        await tools.log(self.client, f"{i} people have been given the member role")


async def setup(client):
    await client.add_cog(Commands(client))
