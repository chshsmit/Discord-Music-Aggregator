"""
ApiConnector.py
@author Christopher Smith
@description Class to make requests to needed apis (YouTube, GoogleSheets)
@created 2020-11-15T15:04:31.896Z-08:00
@last-modified 2020-11-16T12:14:22.273Z-08:00
"""

import json
from os import getenv

import gspread
import requests
from oauth2client.service_account import ServiceAccountCredentials


class ApiConnector:
    def __init__(self):
        super(ApiConnector, self).__init__()
        self._key = getenv("GOOGLE_API_KEY")
        self._base_youtube_url = "https://www.googleapis.com/youtube/v3/videos?id={video_id}&key={key}&part=snippet"
        self._scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]
        self._sheets_creds = ServiceAccountCredentials.from_json_keyfile_name(
            "credentials.json", self._scope
        )

    def say_hello(self):
        print("Hello from api connector")

    # ----------------------------------------------------------------------
    # YOUTUBE
    # ----------------------------------------------------------------------

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

        if len(video_data["items"]) != 0:
            return video_data["items"][0]["snippet"]["title"]

        else:
            return None

    # ----------------------------------------------------------------------
    # Sheets
    # ----------------------------------------------------------------------

    def _next_available_row(self, sheet):
        str_list = list(filter(None, sheet.col_values(1)))
        return len(str_list) + 1

    def insert_new_songs(self, songs):
        client = gspread.authorize(self._sheets_creds)

        sheet = client.open("Music Aggregator").sheet1

        with open("output.json", "w") as out:
            json.dump(songs, out, indent=4)

        rows = [[song["link"], song["title"]] for song in songs if song != None]

        sheet.insert_rows(rows, self._next_available_row(sheet))

    def get_all_current_links_in_sheet(self):
        client = gspread.authorize(self._sheets_creds)
        sheet = client.open("Music Aggregator").sheet1

        all_links = [song["LINK"] for song in sheet.get_all_records()]

        return all_links
