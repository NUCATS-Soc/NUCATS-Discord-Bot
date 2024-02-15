from typing import TYPE_CHECKING

import discord
from discord.ext import commands

import ids
import tools

if TYPE_CHECKING:
    from discord import Message, Member, Guild
    from discord.client import Bot


class Events(commands.Cog):
    def __init__(self, client: "Bot"):
        self.client = client

    # DMs user when they join the server

    @commands.Cog.listener()
    async def on_member_join(self, member: "Member"):
        try:
            await member.send(
                f"Hi {member.name}, welcome to the NUCATS Discord server!\n"
                f"To gain access to the rest of the server, type ``!auth`` in the ❗┃auth-here┃❗ channel\n"
                f"If you have any problems, message @tinyTim567#2879 (Tom | Secretary)"
            )
        except Exception as _:
            c = self.client.get_channel(ids.auth_channel)
            await c.send(f"Hi {member.mention}, welcome to the NUCATS Discord server!\n"
                         f"It seems like your privacy settings are preventing our bot messaging you.\n"
                         f"Please change your settings and type ``!auth`` in this channel.")

        await tools.log(self.client, f"``{member}`` joined the server")

    @commands.Cog.listener()
    async def on_member_remove(self, member: "Member"):
        await tools.log(self.client, f"``{member}`` left the server")

    @commands.Cog.listener()
    async def on_member_ban(self, _: "Guild", member: "Member"):
        await tools.log(self.client, f"``{member}`` was banned from the server")

    @commands.Cog.listener()
    async def on_member_unban(self, _: "Guild", member: "Member"):
        await tools.log(self.client, f"``{member}`` was unbanned from the server")

    @commands.Cog.listener()
    async def on_message_delete(self, message: "Message"):
        embed = discord.Embed(description=message.content)

        channel = self.client.get_channel(ids.bot_log_channel)
        await channel.send(f"``{message.author}``'s message in **{message.channel}** was deleted", embed=embed)
        await tools.log_to_server(f"{message.author}'s message in {message.channel} was deleted")

    @commands.Cog.listener()
    async def on_message_edit(self, old_message: "Message", new_message: "Message"):
        embed = discord.Embed(title="Old Message:", description=old_message.content)
        embed.add_field(name="New message:", value=new_message.content)

        channel = self.client.get_channel(ids.bot_log_channel)
        await channel.send(f"``{old_message.author}``'s message in **{old_message.channel}** was edited", embed=embed)
        await tools.log_to_server(f"{old_message.author}'s message in {old_message.channel} was edited")


async def setup(client: "Bot"):
    await client.add_cog(Events(client))
