import tools
from discord.ext import commands

auth_channel = 1011294492869001327


class OnMemberJoin(commands.Cog):
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
            c = self.client.get_channel(auth_channel)
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


async def setup(client):
    await client.add_cog(OnMemberJoin(client))
