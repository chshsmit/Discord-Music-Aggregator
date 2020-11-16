import os
import re
from random import choice

import discord
import requests
from dotenv import load_dotenv

from ApiConnector import ApiConnector
from utils import get_all_urls, get_video_id, is_youtube_url

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)


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

    api_connector = ApiConnector()

    urls_in_message = get_all_urls(message_content=message.content)
    youtube_ids = [get_video_id(url) for url in urls_in_message if is_youtube_url(url)]

    if len(youtube_ids) == 0:
        await message.channel.send("No Youtube URLs were provided")
        return

    video_names = [api_connector.get_video_name(video_id) for video_id in youtube_ids]

    # count = 0
    # for url in urls_in_message:
    #     if is_youtube_url(url):
    #         count += 1

    await message.channel.send(
        f"The names of the provided youtube videos: {video_names}"
    )


client.run(TOKEN)
