# NUCATS-Discord-Bot

![NUCATS Logo](https://raw.githubusercontent.com/NUCATS-Soc/NUCATS-Discord-Bot/main/github/github_banner.png)

This repository contains the discord bot for managing the NUCATS discord server. It includes features for authenticating
users, managing server roles and logging server updates.

_NUCATS are Newcastle University's computing and technology society. For more information see: https://linktr.ee/nucats_

## Commands

### General commands

- `!auth` - Starts the authentication process.
- `!flip` - Flips a coin.
- `!nucat` - Gets a random image of a cat.
- `!nudog` - Gets a random image of a dog.
- `!ran` - Returns a random number between two given values.
- `!rules` - Displays the server rules.
- `!give_member` - Assigns the member role. Can only be executed by committee members.
- `!verified` - Returns a list of verified members display names and ids. Can only be executed by committee members.
- `!pronouns` - DMs a user with options to change their preferred pronouns.

### Codewars

Commands for managing codewars. These can only be executed in the codewars channel.

- `!challenge` - Sets and announces the next challenge for codewars.
- `!draw` - Draws the winner of the challenge.
- `!join` - Links a given codewars account to the server member.
- `!list_stat` - Returns how many people have completed the current challenge.

## Configuration

The bot reads its configuration from the environment variables.
It is also possible to provide an `.env` file to obtain the same effect.

A sample `.env.dist` file has been provided with all accepted values.
Rename it file to `.env` and fill in the required values.

> **Note:**  
> Environment variables take precedence over the `.env` file.

The following values are required:

- `TOKEN` - The discord bot token.
- `GOOGLE_AUTH_PASSWORD` - The path to the google service account credentials file.
