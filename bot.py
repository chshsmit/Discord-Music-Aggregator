import os
import re
from random import choice

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")
URL_REGEX = "(?P<url>https?://[^\s]+)"
YOUTUBE_REGEX = "^(https?\:\/\/)?((www\.)?youtube\.com|youtu\.?be)\/.+$"

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)


def get_all_urls(message_content: str) -> list:
    """
    Description:
        Returns a list of all the urls in a message

    Args:
        message_content (str): The message

    Returns:
        list: The list of urls
    """

    return re.findall(URL_REGEX, message_content)


def is_youtube_url(url: str) -> bool:
    """
    Description:
        Check if the message was a youtube url

    Args:
        url (string): The url to check

    Returns:
        bool: Whether or not it was a YouTube URL
    """

    return re.search(YOUTUBE_REGEX, url)


@client.event
async def on_ready():

    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f"{client.user} is connected to the following guild:\n"
        f"{guild.name}(id: {guild.id})"
    )

    for channel in guild.channels:
        if channel.type == "Text" and channel.name == "bot-test":
            break

    print(f"We are using this channel: {channel.name}")
    messages = await channel.history().flatten()

    for message in messages:
        urls = get_all_urls(message.content)
        for url in urls:
            if is_youtube_url(url):
                print(url)


@client.event
async def on_message(message):
    if message.author == client.user or message.channel.name != "bot-test":
        return

    urls_in_message = get_all_urls(message_content=message.content)

    count = 0
    for url in urls_in_message:
        if is_youtube_url(url):
            count += 1

    await message.channel.send(f"Number of Youtube URLS Provided: {count}")


client.run(TOKEN)
