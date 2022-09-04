import discord

import ids
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
                f"To gain access to the rest of the server, type ``!auth`` in the ❗┃auth-here┃❗ channel"
            )
        except Exception as e:
            c = self.client.get_channel(ids.auth_channel)
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

        channel = self.client.get_channel(ids.bot_logs_channel)
        await channel.send(f"``{message.author}``'s message in **{message.channel}** was deleted", embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, old_message, new_message):
        embed = discord.Embed(title="Old Message:", description=old_message.content)
        embed.add_field(name="New message:", value=new_message.content)

        channel = self.client.get_channel(ids.bot_logs_channel)
        await channel.send(f"``{old_message.author}``'s message in **{old_message.channel}** was edited", embed=embed)


async def setup(client):
    await client.add_cog(Events(client))
