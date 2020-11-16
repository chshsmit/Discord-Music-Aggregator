"""
ApiConnector.py
@author Christopher Smith
@description Class to make requests to needed apis (YouTube, GoogleSheets)
@created 2020-11-15T15:04:31.896Z-08:00
@last-modified 2020-11-15T18:11:00.291Z-08:00
"""

from os import getenv

import requests


class ApiConnector:
    def __init__(self):
        self._key = getenv("GOOGLE_API_KEY")
        self._base_youtube_url = "https://www.googleapis.com/youtube/v3/videos?id={video_id}&key={key}&part=snippet"

    def get_video_name(self, video_id: str) -> str:
        """
        Description:
            Return the name of a youtube video

        Args:
            video_id (str): The id of the Youtube video

        Returns:
            str: The name of the Youtube video
        """

        url = self._base_youtube_url.format(video_id=video_id, key=self._key)
        response = requests.get(url)

        video_data = response.json()

        return video_data["items"][0]["snippet"]["title"]
