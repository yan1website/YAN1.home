import requests
import feedparser
import json
import random

SHEET_ID = "1qkFOAcrXXBjbAJoHLorSyTXMpPrRfBoX5DDGGstiP8M"
SHEET_QUERY_URL = (
    "https://docs.google.com/spreadsheets/d/"
    + SHEET_ID
    + "/gviz/tq"
)


def sheet_query(query):

    response = requests.get(
        SHEET_QUERY_URL,
        params={
            "tqx": "out:json",
            "tq": query
        },
        timeout=15
    )

    response.raise_for_status()

    payload = response.text
    payload = payload[payload.index("{"):payload.rindex("}") + 1]

    return json.loads(payload)


def get_random_channel_id():

    count_data = sheet_query("select count(H) where H is not null")
    count_cell = count_data["table"]["rows"][0]["c"][0]
    channel_count = int(count_cell.get("v", 0)) if count_cell else 0

    if channel_count == 0:
        raise ValueError("Column H does not contain any channel IDs")

    random_offset = random.randrange(channel_count)
    channel_data = sheet_query(
        "select H where H is not null limit 1 offset "
        + str(random_offset)
    )
    channel_cell = channel_data["table"]["rows"][0]["c"][0]
    channel_id = str(channel_cell.get("v", "")).strip() if channel_cell else ""

    if not channel_id:
        raise ValueError("Selected row in column H is empty")

    return channel_id, random_offset


def get_youtube_videos():

    channel_id, random_offset = get_random_channel_id()
    rss_url = (
        "https://www.youtube.com/feeds/videos.xml"
        "?channel_id=" + channel_id
    )

    response = requests.get(
        rss_url,
        headers={
            "User-Agent": "Mozilla/5.0"
        },
        timeout=15
    )

    response.raise_for_status()

    feed = feedparser.parse(
        response.content
    )

    videos = []

    for entry in feed.entries:

        video_id = entry.get(
            "yt_videoid"
        )

        if not video_id:
            continue

        videos.append({
            "id": video_id,

            "title": entry.get(
                "title",
                "Untitled"
            ),

            "published": entry.get(
                "published",
                ""
            ),

            "url":
                "https://www.youtube.com/watch?v="
                + video_id,

            "embed_url":
                "https://www.youtube.com/embed/"
                + video_id
        })

    return videos, channel_id, random_offset


try:

    videos, channel_id, random_offset = get_youtube_videos()

    print(
        json.dumps({
            "success": True,
            "videos": videos,
            "selected_offset": random_offset,
            "selected_channel_id": channel_id
        })
    )

except Exception as e:

    print(
        json.dumps({
            "success": False,
            "error": str(e)
        })
    )