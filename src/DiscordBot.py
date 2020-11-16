"""
DiscordBot.py
@author Christopher Smith
@description 
@created 2020-11-14T11:51:16.918Z-08:00
@last-modified 2020-11-16T13:08:11.002Z-08:00
"""

# -------------------------------------------------------------------

import os

import discord
from dotenv import load_dotenv

from ApiConnector import ApiConnector
from utils import get_all_urls, get_video_id, is_youtube_url

# -------------------------------------------------------------------


class DiscordBot(discord.Client):
    def __init__(self, guild, token):
        super().__init__()
        self._api_connector = ApiConnector()
        self._guild = guild
        self._token = token

    # -------------------------------------------------------------------

    def get_all_video_info(self, url):
        """
        Description:
            Getting the information for a YouTube video, returns the link and title

        Args:
            url (str): The url of the YouTube video

        Returns:
            [dict]: A dictionary containing the link and title of the provided url
                Example: {"link": "examplelink.com", "title": "Example Video Title"}
        """

        video_id = get_video_id(url)
        video_name = self._api_connector.get_video_name(video_id)

        if video_name == None:
            return None

        return {"link": url, "title": video_name}

    # -------------------------------------------------------------------

    async def on_ready(self):
        """
        Description:
            Always runs when the bot first starts
        """

        for guild in self.guilds:
            if guild.name == self._guild:
                break

        print(
            f"{self.user} is connected to the following guild:\n"
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

        current_links_in_sheet = self._api_connector.get_all_current_links_in_sheet()

        need_to_add = []
        for url in current_urls:
            if url not in current_links_in_sheet:
                all_video_info = self.get_all_video_info(url)

                if all_video_info != None:
                    need_to_add.append(all_video_info)

        if len(need_to_add) > 0:
            self._api_connector.insert_new_songs(need_to_add)
        else:
            print("There was nothing to add on startup")

    # -------------------------------------------------------------------

    async def on_message(self, message: discord.Message) -> None:
        """
        Description:
            This will run whenever a message is sent in the "bangerz" channel. It
            parses the message for any YouTube urls and adds them to the google sheet
            where all of the songs are being aggregated

        Args:
            message (discord.Message): The discord message that was sent
        """
        if message.author == self.user or message.channel.name != "bangerz":
            return

        urls_in_message = get_all_urls(message_content=message.content)

        youtube_urls = [url for url in urls_in_message if is_youtube_url(url)]

        youtube_ids = [get_video_id(url) for url in youtube_urls]

        if len(youtube_urls) == 0:
            return

        all_songs = [self.get_all_video_info(url) for url in youtube_urls]

        self._api_connector.insert_new_songs(
            [song for song in all_songs if song != None]
        )

        song = "song" if len(all_songs) == 1 else "songs"

        message_to_send = f"I added {len(all_songs)} {song} to the sheet"
        print(message_to_send)
        await message.channel.send(message_to_send)

    # -------------------------------------------------------------------

    def run_bot(self):
        """
        Description:
            Running the bot
        """

        self.run(self._token)
