import discord
from discord.ext import commands
import re

log_channel_id = 1011294949679059015


async def log(client, value):
    log_message = client.get_channel(log_channel_id)
    await log_message.send(str(value))


async def check_student_number(m):
    if len(m) != 8:
        return False
    regex = r'^([A-C|a-c])\d{7}$'
    if re.match(regex, m):
        return True
    else:
        return False


async def user_input_dm(client, ctx, str):
    while True:
        msg = await client.wait_for("message")
        if ctx.author == msg.author and isinstance(msg.channel, discord.channel.DMChannel):
            if msg.content.lower() == str.lower() or re.match(str, msg.content.lower()):
                break
            else:
                await ctx.author.send("Invalid input, please try again")
    return msg
