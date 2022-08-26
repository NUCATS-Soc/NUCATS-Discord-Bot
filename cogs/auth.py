import discord
from discord.ext import commands

import tools
import random
import string
import smtplib

with open("auth_password.txt") as file:
    auth_pw = file.read()

# Server role ids
server_id = 1011277165872021504
auth_channel = 1011294492869001327

verified_role = 1011283236497932318

first_year_role = 1011278798995591238
second_year_role = 1011278845825003602
third_year_role = 1011278888841777222
fourth_year_role = 1011278996291465378
placement_year_role = 1011279029443244062
alumni_role = 1011279128445587556
postgrad_role = 1011279081263861791

he_him_role = 1012485842691969116
she_her_role = 1012486225745154068
they_them_role = 1012486431421247508


class Authentication(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def auth(self, ctx):
        await tools.log(self.client, str(ctx.author) + " has begun the authentication")

        # Gets and checks the users student number

        await ctx.author.send("Thank you for starting the NUCATS authentication process.\n" +
                              "Step 1/6: Please enter your university student number (i.e. B8028969 or C1023937).")

        username = await tools.user_input_dm(self.client, ctx, r"^([A-C|a-c])\d{7}$")

        # Generates a random auth code and emails this to the user

        authCode = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8))
        await ctx.author.send(
            "Step 2/6: We have emailed you a verification code to: " + username.content + "@ncl.ac.uk \n" +
            "Please copy and paste it below.\n" +
            "This email may be in your junk mail.")
        sent_from = "nucats.auth.no.reply@gmail.com"
        to = [username.content + "@ncl.ac.uk"]
        body = "Hello " + str(
            ctx.author) + ". Please copy and paste the following code into the discord private chat\n\n" + authCode
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
        except discord.ClientException as e:
            await ctx.author.send("Something went wrong. Please retry authentication or contact an admin.")

        await tools.user_input_dm(self.client, ctx, authCode)

        # Gets the user to accept the server rules

        await ctx.author.send("Step 3/6: Please read our rules and type agree to agree with them.")
        with open("rules.txt") as f:
            lines = f.read()
        await ctx.author.send(lines)
        await ctx.author.send("**Please read the rules and type agree to agree with them**")
        await tools.user_input_dm(self.client, ctx, "agree")

        # Gets the user to enter their real name to use on the server

        await ctx.author.send(
            "Step 4/6: As part of the rules of the NUCATS server we require everyone's Discord name " +
            "to be their actual name.\n" +
            "Please enter your preferred name below.")
        nickname = await tools.user_input_dm(self.client, ctx, r"\w{1,14}$")
        await self.client.get_guild(server_id).get_member(nickname.author.id).edit(
            nick=nickname.content)

        # Sets user pronouns

        await ctx.author.send('''Step 5/6: Please select your preferred pronouns by entering the corresponding number:
                      1 - he/him
                      2 - she/her
                      3 - they/them
                    If your Pronoun is not here please message committee and we will sort it :)''')
        pronouns = await tools.user_input_dm(self.client, ctx, r"[1-3]{1}$")
        member = self.client.get_guild(server_id).get_member(pronouns.author.id)
        role = discord.utils.get(self.client.get_guild(server_id).roles,
                                 id=they_them_role)
        if pronouns.content == "1":
            role = discord.utils.get(self.client.get_guild(server_id).roles,
                                     id=he_him_role)
        elif pronouns.content == "2":
            role = discord.utils.get(self.client.get_guild(server_id).roles,
                                     id=she_her_role)
        elif pronouns.content == "3":
            role = discord.utils.get(self.client.get_guild(server_id).roles,
                                     id=they_them_role)
        await member.add_roles(role)

        # Sets users stage

        await ctx.author.send('''Step 6/6: Please select which stage you are in by entering the corresponding number:)
                  1 - first
                  2 - second
                  3 - third
                  4 - fourth
                  5 - placement
                  6 - post grad
                  7 - alumni''')
        stage = await tools.user_input_dm(self.client, ctx, r"[1-6]{1}$")
        member = self.client.get_guild(server_id).get_member(stage.author.id)
        role = discord.utils.get(self.client.get_guild(server_id).roles,
                                 id=first_year_role)
        if stage.content == "1":
            role = discord.utils.get(self.client.get_guild(server_id).roles,
                                     id=first_year_role)
        elif stage.content == "2":
            role = discord.utils.get(self.client.get_guild(server_id).roles,
                                     id=second_year_role)
        elif stage.content == "3":
            role = discord.utils.get(self.client.get_guild(server_id).roles,
                                     id=third_year_role)
        elif stage.content == "4":
            role = discord.utils.get(self.client.get_guild(server_id).roles,
                                     id=fourth_year_role)
        elif stage.content == "5":
            role = discord.utils.get(self.client.get_guild(server_id).roles,
                                     id=placement_year_role)
        elif stage.content == "6":
            role = discord.utils.get(self.client.get_guild(server_id).roles,
                                     id=postgrad_role)
        elif stage.content == "7":
            role = discord.utils.get(self.client.get_guild(server_id).roles,
                                     id=alumni_role)
        await member.add_roles(role)
        role = discord.utils.get(self.client.get_guild(server_id).roles,
                                 id=verified_role)
        await member.add_roles(role)
        await ctx.author.send("You are now authenticated and have full access to the server!")
        await tools.log(self.client, f"{username.author} has authenticated with username {username.content}, "
                                     f"chose their nickname as {nickname.content}, chose option {pronouns.content} "
                                     f"as their pronouns, and chose option {stage.content} for their stage.")


async def setup(client):
    await client.add_cog(Authentication(client))
