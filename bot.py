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

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
api_connector = ApiConnector()


def get_all_video_info(url):
    video_id = get_video_id(url)
    video_name = api_connector.get_video_name(video_id)

    if video_name == None:
        return None

    return {"link": url, "title": video_name}


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
        if channel.name == "bangerz":
            break

    print(f"We are using this channel: {channel.name}")
    messages = await channel.history().flatten()

    current_urls = set()
    for message in messages:
        urls = get_all_urls(message.content)
        for url in urls:
            if is_youtube_url(url):
                current_urls.add(url)

    current_links_in_sheet = api_connector.get_all_current_links_in_sheet()

    # TODO: Add filter here to remove all Nones
    need_to_add = []
    for url in current_urls:
        if url not in current_links_in_sheet:
            need_to_add.append(get_all_video_info(url))

    if len(need_to_add) > 0:
        api_connector.insert_new_songs(need_to_add)
    else:
        print("There was nothing to add")


@client.event
async def on_message(message):
    if message.author == client.user or message.channel.name != "bangerz":
        return

    urls_in_message = get_all_urls(message_content=message.content)
    youtube_ids = [get_video_id(url) for url in urls_in_message if is_youtube_url(url)]

    youtube_urls = [url for url in urls_in_message if is_youtube_url(url)]

    if len(youtube_urls) == 0:
        await message.channel.send("No Youtube URLs were provided")
        return

    all_songs = [get_all_video_info(url) for url in youtube_urls]

    api_connector.insert_new_songs([song for song in all_songs if song != None])

    song = "song" if len(all_songs) == 1 else "songs"

    await message.channel.send(f"I added {len(all_songs)} {song} to the sheet")


client.run(TOKEN)
