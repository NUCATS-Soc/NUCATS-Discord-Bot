import asyncio
import re
import discord
import mysql.connector
from mysql.connector import Error
from datetime import datetime

import database
import ids


async def query_insert(string):
    """ Queries the database with a given SQL INSERT command

    :param string: SQL INSERT command
    :return: True if query succeeded, False if query failed
    """
    try:
        connection = mysql.connector.connect(host=database.host,
                                             database=database.database,
                                             user=database.user,
                                             password=database.password)
        if connection.is_connected():
            db_info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_info)
            cursor = connection.cursor()
            cursor.execute(string)
            connection.commit()
            print(cursor.rowcount, "Record inserted successfully into table")
            cursor.close()
            return True
    except Error as e:
        print("Error while connecting to MySQL", e)
        return False
    finally:
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")


async def query_select(string):
    """ Queries the database with a given SELECT SQL command

    :param string: SQL SELECT query
    :return: Result of query
    """
    try:
        connection = mysql.connector.connect(host=database.host,
                                             database=database.database,
                                             user=database.user,
                                             password=database.password)
        if connection.is_connected():
            db_info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_info)
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
    """Writes to the log channel and the server log

    :param client: Client object
    :param value: Value to be logged
    """
    log_message = client.get_channel(ids.bot_log_channel)
    await log_message.send(str(value))
    format_chars = ["*", "`"]
    for char in format_chars:
        value = value.replace(char, "")

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {value}")


async def check_student_number(student_number):
    """Checks if a given student number is valid

    :param student_number: String to be checked
    :return: True if valid, false if invalid
    """
    if len(student_number) != 8:
        return False
    regex = r'^([A-C|a-c])\d{7}$'
    if re.match(regex, student_number):
        return True
    else:
        return False


async def user_input_dm(client, ctx, reg_str, timeout=None):
    """Gets input from the user and performs validation checks

    :param client: Client object
    :param ctx: Current context
    :param reg_str: String to check input against. Can be string to match exactly or a regular expression
    :param timeout: (Optional) Time in seconds until request for input fails
    :return: Validated message or None if validation failed
    """

    def check(message):
        return ctx.author == message.author and isinstance(message.channel, discord.channel.DMChannel) and \
               (message.content.lower() == str.lower() or re.match(reg_str, message.content.lower()))

    try:
        msg = await client.wait_for("message", timeout=timeout, check=check)
    except asyncio.TimeoutError:
        await ctx.author.send("You did not respond in time. Please try again. ")
        return None
    else:
        return msg


async def get_user_pronouns(client, ctx, timeout=60.0):
    """Gets the users preferred pronouns

    :param client: Client object
    :param ctx: Current context
    :param timeout: (Optional) Time in seconds until request fails
    :return: Users reaction to post and user object. On failure returns None, None
    """
    gender_message = await ctx.author.send("Please select your preferred pronouns by reacting to this post \n" +
                                           "♂ - He/him \n" +
                                           "♀ - She/her \n" +
                                           "⚧ - They/them \n" +
                                           "If your Pronoun is not here, please message committee and we will sort it "
                                           ":) \n" +
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
