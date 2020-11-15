"""
utils.py
@author Christopher Smith
@description Utility functions
@created 2020-11-15T14:56:05.531Z-08:00
@last-modified 2020-11-15T15:15:32.916Z-08:00
"""

from re import findall as re_findall
from re import search as re_search
from urllib.parse import parse_qs, urlparse


def get_all_urls(message_content: str) -> list:
    """
    Description:
        Returns a list of all the urls in a message

    Args:
        message_content (str): The message

    Returns:
        list: The list of urls
    """

    URL_REGEX = "(?P<url>https?://[^\s]+)"
    return re_findall(URL_REGEX, message_content)


def is_youtube_url(url: str) -> bool:
    """
    Description:
        Check if the message was a youtube url

    Args:
        url (string): The url to check

    Returns:
        bool: Whether or not it was a YouTube URL
    """

    YOUTUBE_REGEX = "^(https?\:\/\/)?((www\.)?youtube\.com|youtu\.?be)\/.+$"
    return re_search(YOUTUBE_REGEX, url)


def get_video_id(youtube_url: str) -> str:
    """
    Description:
        Getting the video id of a provided Youtube URL

    Args:
        youtube_url (str): The url of the youtube video

    Returns:
        str: The id of the youtube video
    """

    query = urlparse(youtube_url)
    if query.hostname == "youtu.be":
        return query.path[1:]
    if query.hostname in ("www.youtube.com", "youtube.com"):
        if query.path == "/watch":
            p = parse_qs(query.query)
            return p["v"][0]
        if query.path[:7] == "/embed/":
            return query.path.split("/")[2]
        if query.path[:3] == "/v/":
            return query.path.split("/")[2]

    return None
