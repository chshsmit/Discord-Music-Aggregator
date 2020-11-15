"""
YoutubeApiConnector.py
@author Christopher Smith
@description Class to make a request to the Youtube API
@created 2020-11-15T15:04:31.896Z-08:00
@last-modified 2020-11-15T15:14:28.446Z-08:00
"""

from os import getenv

import requests


class YoutubeApiConnector:
    def __init__(self):
        self._key = getenv("YOUTUBE_API_KEY")
        self._base_url = "https://www.googleapis.com/youtube/v3/videos?id={video_id}&key={key}&part=snippet"

    def get_video_name(self, video_id: str) -> str:
        """
        Description:
            Return the name of a youtube video

        Args:
            video_id (str): The id of the Youtube video

        Returns:
            str: The name of the Youtube video
        """

        url = self._base_url.format(video_id=video_id, key=self._key)
        response = requests.get(url)

        video_data = response.json()

        return video_data["items"][0]["snippet"]["title"]
