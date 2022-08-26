import discord
from discord.ext import commands

import ids
import tools
import random
import string
import smtplib

with open("auth_password.txt") as file:
    auth_pw = file.read()

class Authentication(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def auth(self, ctx):
        if ctx.channel.id != ids.auth_channel:
            return

        await tools.log(self.client, "``" + str(ctx.author) + "`` has begun the authentication")

        # Gets and checks the users student number

        await ctx.author.send("Thank you for starting the NUCATS authentication process.\n" +
                              "Step 1/6: Please enter your university student number (i.e. B8028969 or C1023937):")

        username = await tools.user_input_dm(self.client, ctx, r"^([A-C|a-c])\d{7}$")

        # Generates a random auth code and emails this to the user

        authCode = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8))

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

        await ctx.author.send(
            "Step 2/6: We have emailed a verification code to: " + username.content + "@ncl.ac.uk \n" +
            "Please copy and paste it below.\n" +
            "This email may be in your junk mail.")

        await tools.user_input_dm(self.client, ctx, authCode)

        # Gets the user to accept the server rules

        await ctx.author.send("Step 3/6: Please read our rules and type agree to agree with them.")

        with open("rules.txt") as f:
            lines = f.read()

        await ctx.author.send(lines)
        await ctx.author.send("**Please read the rules and type ``agree`` to accept them**")
        await tools.user_input_dm(self.client, ctx, "agree")

        # Gets the user to enter their real name to use on the server

        await ctx.author.send(
            "Step 4/6: As part of the rules of the NUCATS server we require everyone's Discord name " +
            "to be their actual name.\n" +
            "Please enter your name below.")

        nickname = await tools.user_input_dm(self.client, ctx, r"\w{1,14}$")
        await self.client.get_guild(ids.server_id).get_member(nickname.author.id).edit(
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
                  1 - Stage 1 (First year)
                  2 - Stage 2
                  3 - Stage 3
                  4 - Stage 4 
                  5 - Placement
                  6 - Post Grad
                  7 - Alumni''')
        stage = await tools.user_input_dm(self.client, ctx, r"[1-7]{1}$")
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

        await ctx.author.send("You are now authenticated and have full access to the server!")
        await tools.log(self.client,
                        f"``{username.author}`` has authenticated with student number ``{username.content}``, "
                        f"chose their nickname as ``{nickname.content}``, "
                        f"chose ``option {pronouns.content}`` "
                        f"as their pronouns, and chose option ``{stage.content}`` for their stage.")


async def setup(client):
    await client.add_cog(Authentication(client))
