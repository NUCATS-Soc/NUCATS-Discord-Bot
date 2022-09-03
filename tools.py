import asyncio
import re
import discord

log_channel_id = 1011294949679059015


async def log(client, value):
    log_message = client.get_channel(log_channel_id)
    await log_message.send(str(value))


async def check_student_number(student_number):
    if len(student_number) != 8:
        return False
    regex = r'^([A-C|a-c])\d{7}$'
    if re.match(regex, student_number):
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


async def get_user_pronouns(client, ctx, timeout=60.0):
    gender_message = await ctx.author.send("Please select your preferred pronouns by reacting to this post \n" +
                                           "♂ - He/him \n" +
                                           "♀ - She/her \n" +
                                           "⚧ - They/them \n" +
                                           "If your Pronoun is not here, please message committee and we will sort it :) \n" +
                                           "You can change your pronouns later")

    # Reacts to its own post
    emojis = ["♂", "♀", "⚧"]
    for emoji in emojis:
        await gender_message.add_reaction(emoji)

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in emojis

    try:
        reaction, user = await client.wait_for("reaction_add", timeout=timeout, check=check)
    except asyncio.TimeoutError:
        await ctx.author.send("You did not react to the post in time. Type ``!pronouns`` to try again.")
    else:
        return reaction, user
