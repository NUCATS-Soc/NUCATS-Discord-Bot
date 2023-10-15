import random
from typing import TYPE_CHECKING

import requests
from discord.ext import commands

import ids
import tools

if TYPE_CHECKING:
    from discord.client import Bot
    from discord.ext.commands import Context


class CodeWars(commands.Cog):

    def __init__(self, client: "Bot"):
        self.client = client

    @commands.command(brief="Join codewars",
                      description="Type !join username, where username is your codewars account name")
    @commands.guild_only()
    async def join(self, ctx: "Context", username: "str"):
        if ctx.channel.id != ids.codewars_log_channel:
            return

        # Checks user has codewars account
        response = requests.get("https://www.codewars.com/api/v1/users/" + username)
        if response.status_code == 200:
            # Checks if user has already been added
            if await tools.query_select(f"""SELECT * FROM codewars WHERE id = '{ctx.author.id}'""") == []:
                # Adds user to codewars db
                if await tools.query_insert(f"""INSERT INTO codewars VALUES ('{str(ctx.author.id)}', '{username}');"""):
                    # Account added successfully
                    await tools.log(self.client,
                                    f"**CODEWARS** - Added user ``{ctx.author}`` with account ``{username}``")
                    await ctx.channel.send(f"Added ``{username}`` to codewars!")
                else:
                    # Could not access the database
                    await tools.log(self.client,
                                    f"**CODEWARS** - Failed to add user ``{ctx.author}`` with username ``{username}`` "
                                    f"(Failed to update the database)")
                    await ctx.channel.send(f"An error occurred when adding user ``{username}``. Please try again later")
            else:
                # Account already linked to discord user
                await tools.log(self.client,
                                f"**CODEWARS** - Failed to add user ``{ctx.author}`` with account ``{username}`` "
                                f"(Account already registered)")
                await ctx.channel.send(f"User ``{ctx.author}`` has already registered a codewars account")

        else:
            # Account doesn't exist
            await tools.log(self.client, f"**CODEWARS** - API response error: ``{str(response)}``")
            await ctx.channel.send(f"An account could not be found for ``{username}``")

    @commands.command(brief="Draws this weeks winner", description="Draws this weeks winner")
    @commands.has_role(ids.committee_role)
    @commands.guild_only()
    async def draw(self, ctx: "Context"):
        if ctx.channel.id != ids.codewars_log_channel:
            return

        # Gets all registered codewars users
        response = await tools.query_select("""SELECT * FROM codewars;""")
        response_dict = {}

        print(str(response))
        for i in response:
            response_dict[i[0]] = i[1]

        with open("logs/codewars_challenge.txt", "r", encoding="utf-8") as file:
            challenge_id = file.readlines()[-1]

        # Loops until all users have been checked
        while bool(response_dict):
            winner = random.sample(response_dict.keys(), 1)[0]
            winner_username = response_dict.get(winner)

            # Checks user has completed the challenge
            response = requests.get(
                f'https://www.codewars.com/api/v1/users/{winner_username}/code-challenges/completed')
            res_object = response.json()
            for obj in res_object["data"]:
                if obj["id"] == challenge_id:
                    winner = await self.client.fetch_user(winner)
                    await tools.log(self.client, f'**CODEWARS** - ``{winner}`` has won the challenge')
                    await ctx.channel.send(f'<@{winner.id}> has completed the challenge so wins £5!!!')
                    return
            del response_dict[winner]

        await tools.log(self.client, "**CODEWARS** - No winner could be drawn")
        await ctx.channel.send("No one has completed this weeks challenge 😭")

    @commands.command(brief="Sets and announces this weeks challenge",
                      description="Sets this weeks challenge and then posts an announcement")
    @commands.has_role(ids.committee_role)
    @commands.guild_only()
    async def challenge(self, ctx: "Context", challenge_id: "str"):
        if ctx.channel.id != ids.bot_log_channel:
            return

        # Checks if the challenge has been used before
        with open("logs/codewars_challenge.txt", "r", encoding="utf-8") as file:
            for line in file:
                if challenge_id == line:
                    await tools.log(self.client, f"Challenge ``{challenge_id}`` has already been used")
                    return

        with open("logs/codewars_challenge.txt", "a", encoding="utf-8") as file:
            file.write("\n" + challenge_id)

        await tools.log(self.client, "Posting challenge...")

        challenge_announcement = self.client.get_channel(ids.codewars_announcements_channel)
        await challenge_announcement.send("🔥  This weeks code wars challenge is now live @here! 🔥 \n"
                                          "✨ Play each week for the chance to win a £5 voucher and improve your coding ability! \n"
                                          f"🛠️ This weeks challenge is https://www.codewars.com/kata/{challenge_id} \n"
                                          "💸 Prize draw and new challenge released every Sunday")

        await tools.log(self.client, f"Challenge ``{challenge_id}`` has been posted")

    @commands.command(aliases=["list_stats", "list", "stat", "stats", "liststat", "liststats"],
                      brief="Lists how many have completed this weeks challenge",
                      description="Lists how many people have completed this weeks challenge")
    @commands.guild_only()
    async def list_stat(self, ctx: "Context"):
        if ctx.channel.id not in ids.codewars_group:
            return

        # Gets the latest challenge
        with open("logs/codewars_challenge.txt", "r", encoding="utf-8") as file:
            challenge_id = file.readlines()[-1]

        # Checks the total amount who have completed the challenge
        response = await tools.query_select("""SELECT * FROM codewars;""")
        response_values = [i[1] for i in response]

        complete = 0
        total = 0
        for k in response_values:
            total = total + 1
            user = str(k)
            response = requests.get(f"https://www.codewars.com/api/v1/users/{user}/code-challenges/completed", timeout=10)
            res_object = response.json()
            try:
                for obj in res_object["data"]:
                    if str(obj["id"]) == challenge_id:
                        complete = complete + 1
            except Exception:
                total = total - 1
        await ctx.channel.send(
            f"**{complete} / {total}** or **{int(100 * (complete / total))}%** have completed the challenge so far!")


async def setup(client: "Bot"):
    await client.add_cog(CodeWars(client))
