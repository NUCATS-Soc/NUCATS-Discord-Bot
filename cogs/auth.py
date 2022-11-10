import discord
from discord.ext import commands
from csv import writer

import ids
import tools
import random
import string
import smtplib

# Gets password for authing with the Google account
with open("auth_password.txt") as file:
    auth_pw = file.read()


class Authentication(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(brief="Starts the auth process",
                      description="Starts the auth process. Can only be executed in the auth channel")
    @commands.guild_only()
    async def auth(self, ctx):
        if ctx.channel.id != ids.auth_channel:
            return

        await tools.log(self.client, "``" + str(ctx.author) + "`` has begun the authentication")

        # Gets the user's student number

        await ctx.author.send("Thank you for starting the NUCATS authentication process.\n" +
                              "**Step 1/7** \n"
                              "Please enter your university student number (i.e. 180289690 or 210239379):")

        student_number = await tools.user_input_dm(self.client, ctx, r"^\d{9}$", 180.0)
        if student_number is None:
            await tools.log(self.client, "``" + str(ctx.author) + "`` did not respond to auth in time")
            return

        # Gets the users email address

        await ctx.author.send(
            "Thank you.\n**Step 2/7**\nPlease enter the first part of your university email address (i.e. J.L.Smith2 or C10239379):")

        username = await tools.user_input_dm(self.client, ctx, r"^[0-9,a-z,A-Z,.]{1,30}$", 60.0)
        if username is None:
            await tools.log(self.client, "``" + str(ctx.author) + "`` did not respond to auth in time")
            return

        # Generates a random auth code and emails this to the user

        auth_code = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8))

        sent_from = "nucats.auth.no.reply@gmail.com"
        to = [username.content + "@ncl.ac.uk"]
        body = ("Hello " + str(
            ctx.author) + ". Please copy and paste the following code into the discord private chat\n\n" + auth_code)
        subject = "Verification Code"
        email_text = """From: %s\r\nTo: %s\r\nSubject: %s\r\n\
                    %s
                    """ % (sent_from, ", ".join(to), subject, body)

        try:
            server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            server.ehlo()
            server.login("nucats.auth.no.reply@gmail.com", auth_pw)
            server.sendmail("nucats.auth.no.reply@gmail.com", to, email_text)
            server.close()
        except discord.ClientException:
            await ctx.author.send("Something went wrong. Please retry authentication or contact committee.")

        await ctx.author.send(
            "**Step 3/7** \nWe have emailed a verification code to: ``" + username.content + "@ncl.ac.uk`` \n" +
            "Please copy and paste it below.\n" +
            "(This email may be in your junk mail)")

        if await tools.user_input_dm(self.client, ctx, auth_code, 240.0) is None:
            await tools.log(self.client, "``" + str(ctx.author) + "`` did not respond to auth in time")
            return

        # Gets the user to accept the server rules

        await ctx.author.send("**Step 4/6** \nPlease read our rules and type ``agree`` to accept them.")

        with open("rules.txt") as f:
            lines = f.read()

        await ctx.author.send(lines)
        await ctx.author.send("**Please read the rules and type ``agree`` to accept them**")
        await tools.user_input_dm(self.client, ctx, "agree")

        # Gets the user to enter their real name to use on the server

        if await ctx.author.send(
                "**Step 5/7** \nAs part of the rules of the NUCATS server we require everyone's Discord name " +
                "to be their actual name.\n" +
                "Please enter your preferred name below:") is None:
            await tools.log(self.client, "``" + str(ctx.author) + "`` did not respond to auth in time")
            return

        nickname = await tools.user_input_dm(self.client, ctx, r"\w{1,14}$", 60.0)
        if nickname is None:
            await tools.log(self.client, "``" + str(ctx.author) + "`` did not respond to auth in time")
            return

        await self.client.get_guild(ids.server_id).get_member(nickname.author.id).edit(
            nick=nickname.content)

        # Sets user pronouns

        await ctx.author.send("**Step 6/7**")
        reaction, user = await tools.get_user_pronouns(self.client, ctx, 90.0)
        if reaction is None or user is None:
            await tools.log(self.client, "``" + str(ctx.author) + "`` did not respond to auth in time")
            return

        member = self.client.get_guild(ids.server_id).get_member(user.id)

        if str(reaction) == "♂":
            role = discord.utils.get(self.client.get_guild(ids.server_id).roles, id=ids.he_him_role)
            pronoun = "He/him"

        elif str(reaction) == "♀":
            role = discord.utils.get(self.client.get_guild(ids.server_id).roles, id=ids.she_her_role)
            pronoun = "She/her"

        else:
            role = discord.utils.get(self.client.get_guild(ids.server_id).roles, id=ids.they_them_role)
            pronoun = "They/them"

        await member.add_roles(role)

        # Sets users stage

        await ctx.author.send(
            "**Step 7/7** \n" +
            "Please select which stage you are in by entering the corresponding number: \n" +
            "1 - Stage 1 (First year) \n" +
            "2 - Stage 2 \n" +
            "3 - Stage 3 \n" +
            "4 - Stage 4 \n" +
            "5 - Placement \n" +
            "6 - Post Grad \n" +
            "7 - Alumni")
        stage = await tools.user_input_dm(self.client, ctx, r"[1-7]{1}$", 60.0)
        if stage is None:
            await tools.log(self.client, "``" + str(ctx.author) + "`` did not respond to auth in time")
            return

        member = self.client.get_guild(ids.server_id).get_member(stage.author.id)
        role = discord.utils.get(self.client.get_guild(ids.server_id).roles, id=ids.first_year_role)

        if stage.content == "1":
            role = discord.utils.get(self.client.get_guild(ids.server_id).roles, id=ids.first_year_role)

        elif stage.content == "2":
            role = discord.utils.get(self.client.get_guild(ids.server_id).roles, id=ids.second_year_role)

        elif stage.content == "3":
            role = discord.utils.get(self.client.get_guild(ids.server_id).roles, id=ids.third_year_role)

        elif stage.content == "4":
            role = discord.utils.get(self.client.get_guild(ids.server_id).roles, id=ids.fourth_year_role)

        elif stage.content == "5":
            role = discord.utils.get(self.client.get_guild(ids.server_id).roles, id=ids.placement_year_role)

        elif stage.content == "6":
            role = discord.utils.get(self.client.get_guild(ids.server_id).roles, id=ids.postgrad_role)

        elif stage.content == "7":
            role = discord.utils.get(self.client.get_guild(ids.server_id).roles, id=ids.alumni_role)

        await member.add_roles(role)

        # Gives the user verified role

        role = discord.utils.get(self.client.get_guild(ids.server_id).roles, id=ids.verified_role)
        await member.add_roles(role)

        await ctx.author.send("**🎉 You are now authenticated! 🎉**\n" +
                              "You should now have access to the server. \n" +
                              "If you have bought a membership, you will be give the member role shortly. \n" +
                              "To change your pronouns, type ``!pronouns`` in this chat. \n" +
                              "Channels have descriptions explaining what they are for and how everything works. " +
                              "If you have any issues, contact committee.")

        # Logs users details
        await tools.log(self.client,
                        f"``{username.author}`` has authenticated \n"
                        f"  - Nickname ``{nickname.content}`` \n"
                        f"  - Student Number ``{student_number.content} \n``"
                        f"  - Email ``{username.content}`` \n"
                        f"  - Stage ``{stage.content}`` \n"
                        f"  - Pronouns ``{pronoun}`` \n"
                        f"  - Id ``{member.id}``"
                        )

        with open("logs/verified_users.csv", "a", newline="") as file:
            file_writer = writer(file)
            file_writer.writerow([member.id, student_number.content])
            file.close()


async def setup(client):
    await client.add_cog(Authentication(client))
