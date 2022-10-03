import random
import requests
from discord.ext import commands

import ids
import tools


class CodeWars(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def join(self, ctx, username):
        if ctx.channel.id != ids.codewars_log_channel:
            return

        # Checks user has codewars account
        response = requests.get("https://www.codewars.com/api/v1/users/" + username)
        if response.status_code == 200:
            # Checks if user has already been added
            if await tools.querySelect(f"""SELECT * FROM codewars WHERE id = '{ctx.author.id}'""") == []:
                # Adds user to codewars db
                await tools.queryInsert(f"""INSERT INTO codewars VALUES ('{str(ctx.author.id)}', '{username}');""")
                await tools.log(self.client, f"CODEWARS - Added user ``{ctx.author}`` with account ``{username}``")
                await ctx.channel.send(f"Added ``{username}`` to codewars!")
            else:
                await tools.log(self.client,
                                f"CODEWARS - Failed to add user ``{ctx.author}`` (Account already registered)")
                await ctx.channel.send(f"User ``{ctx.author}`` has already registered a codewars account")

        else:
            # Account doesn't exist
            await tools.log(self.client, f"CODEWARS - API response error: {str(response)}")
            await ctx.channel.send(f"An account could not be found for ``{username}``")

    @commands.command()
    async def draw(self, ctx):
        if ctx.channel.id != ids.codewars_log_channel:
            return

        response = await tools.querySelect(f"""SELECT * FROM codewars;""")
        responseDict = {}

        print(str(response))
        for i in response:
            responseDict[i[0]] = i[1]

        with open("logs/codewars_challenge.txt", "r") as file:
            challenge_id = file.read()

        # Loops until all users have been checked
        while bool(responseDict):
            winner = random.sample(responseDict.keys(), 1)[0]
            winner_username = responseDict.get(winner)

            response = requests.get(
                f'https://www.codewars.com/api/v1/users/{winner_username}/code-challenges/completed')
            res_object = response.json()
            for obj in res_object["data"]:
                if obj["id"] == challenge_id:
                    winner = await self.client.fetch_user(winner)
                    await tools.log(self.client, f'CODEWARS - ``{winner}`` has won the challenge')
                    await ctx.channel.send(f'<@{winner.id}> has completed the challenge so wins £5!!!')
                    return
            del responseDict[winner]

        await tools.log(self.client, f"CODEWARS - No winner could be drawn")
        await ctx.channel.send("No one has completed this weeks challenge 😭")

    @commands.command()
    async def challenge(self, ctx, challenge_id):
        if ctx.channel.id != ids.bot_log_channel:
            return

        with open("logs/codewars_challenge.txt", "w") as file:
            file.write(challenge_id)

        await tools.log(self.client, f"Posting this weeks challenge")

        challenge_announcement = self.client.get_channel(ids.codewars_announcements_channel)
        await challenge_announcement.send(f"🔥  This weeks code wars challenge is now live @here! 🔥 \n" +
                                          f"✨ Play each week for the chance to win a £5 voucher and improve your coding ability! \n" +
                                          f"🛠️ This weeks challenge is https://www.codewars.com/kata/{challenge_id} \n" +
                                          f"💸 Prize draw and new challenge released every week")

    @commands.command()
    async def listStat(self, ctx):
        response = await tools.querySelect(f"""SELECT * FROM codewars;""")
        responseValues = [i[1] for i in response]

        with open("logs/codewars_challenge.txt", "r") as file:
            challenge_id = file.read()

        complete = 0
        total = 0
        for k in responseValues:
            total = total + 1
            out = False
            user = str(k)
            response = requests.get(f'https://www.codewars.com/api/v1/users/{user}/code-challenges/completed')
            resObject = response.json()
            try:
                for obj in resObject["data"]:
                    if (str(obj["id"]) == challenge_id):
                        complete = complete + 1
            except Exception:
                total = total - 1
        await ctx.channel.send(
            f'**{complete} / {total}** or **{int(100 * (complete / total))}%** have completed the challenge so far!')


async def setup(client):
    await client.add_cog(CodeWars(client))
