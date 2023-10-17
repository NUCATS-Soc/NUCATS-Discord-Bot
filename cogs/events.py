import traceback
import sys

import discord

from config import Config
import tools
from discord.ext import commands


class Events(commands.Cog):
    def __init__(self, client):
        self.client = client

    # DMs user when they join the server

    @commands.Cog.listener()
    async def on_member_join(self, member):
        try:
            await member.send(
                f"Hi {member.name}, welcome to the NUCATS Discord server!\n"
                f"To gain access to the rest of the server, type ``!auth`` in the ❗┃auth-here┃❗ channel\n"
                f"If you have any problems, message @tinyTim567#2879 (Tom | Secretary)"
            )
        except Exception as e:
            c = self.client.get_channel(Config.get("AUTH_CHANNEL"))
            await c.send(f"Hi {member.mention}, welcome to the NUCATS Discord server!\n"
                         f"It seems like your privacy settings are preventing our bot messaging you.\n"
                         f"Please change your settings and type ``!auth`` in this channel.")

        await tools.log(self.client, f"``{member}`` joined the server")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        await tools.log(self.client, f"``{member}`` left the server")

    @commands.Cog.listener()
    async def on_member_ban(self, guild, member):
        await tools.log(self.client, f"``{member}`` was banned from the server")

    @commands.Cog.listener()
    async def on_member_unban(self, guild, member):
        await tools.log(self.client, f"``{member}`` was unbanned from the server")

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        embed = discord.Embed(description=message.content)

        channel = self.client.get_channel(Config.get("BOT_LOG_CHANNEL"))
        await channel.send(f"``{message.author}``'s message in **{message.channel}** was deleted", embed=embed)
        await tools.log_to_server(f"{message.author}'s message in {message.channel} was deleted")

    @commands.Cog.listener()
    async def on_message_edit(self, old_message, new_message):
        embed = discord.Embed(title="Old Message:", description=old_message.content)
        embed.add_field(name="New message:", value=new_message.content)

        channel = self.client.get_channel(Config.get("BOT_LOG_CHANNEL"))
        await channel.send(f"``{old_message.author}``'s message in **{old_message.channel}** was edited", embed=embed)
        await tools.log_to_server(f"{old_message.author}'s message in {old_message.channel} was edited")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command.

        :param ctx: The context used for command invocation.
        :param error: The Exception raised.
        """
        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, 'on_error'):
            return

        ignored = (commands.CommandNotFound, )

        # Allows us to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to on_command_error.
        error = getattr(error, 'original', error)

        # Anything in ignored will return and prevent anything happening.
        if isinstance(error, ignored):
            return

        # All other Errors not returned come here. And we can just print the default TraceBack.
        print(f"Ignoring exception in command {ctx.command}:", file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

async def setup(client):
    await client.add_cog(Events(client))
