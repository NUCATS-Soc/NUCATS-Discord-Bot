import asyncio
import re
import discord
import mysql.connector
from mysql.connector import Error
from datetime import datetime

import database
import ids


async def queryInsert(string):
    try:
        connection = mysql.connector.connect(host=database.host,
                                             database=database.database,
                                             user=database.user,
                                             password=database.password)
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute(string)
            connection.commit()
            print(cursor.rowcount, "Record inserted successfully into table")
            cursor.close()
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")


async def querySelect(string):
    try:
        connection = mysql.connector.connect(host=database.host,
                                             database=database.database,
                                             user=database.user,
                                             password=database.password)
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute(string)
            result = cursor.fetchall()
            return result
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            connection.close()
            cursor.close()
            print("MySQL connection is closed")


async def log(client, value):
    log_message = client.get_channel(ids.bot_log_channel)
    await log_message.send(str(value))
    format_chars = ["*", "`"]
    for char in format_chars:
        value = value.replace(char, "")

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {value}")


async def check_student_number(student_number):
    if len(student_number) != 8:
        return False
    regex = r'^([A-C|a-c])\d{7}$'
    if re.match(regex, student_number):
        return True
    else:
        return False


async def user_input_dm(client, ctx, str, timeout=None):
    def check(msg):
        return ctx.author == msg.author and isinstance(msg.channel, discord.channel.DMChannel) and \
               (msg.content.lower() == str.lower() or re.match(str, msg.content.lower()))

    try:
        msg = await client.wait_for("message", timeout=timeout, check=check)
    except asyncio.TimeoutError:
        await ctx.author.send("You did not respond in time. Please try again. ")
        return None
    else:
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
        return None, None
    else:
        return reaction, user
