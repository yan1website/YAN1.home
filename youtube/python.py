import requests
import feedparser
import json
import random
import sys

SHEET_ID = "1EaWCnp7qrrNI1zrRBKiqg6ss3pSo8WRAan4ZkEi1CQs"
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

    count_data = sheet_query("select count(C) where C is not null")
    count_cell = count_data["table"]["rows"][0]["c"][0]
    channel_count = int(count_cell.get("v", 0)) if count_cell else 0

    if channel_count == 0:
        raise ValueError("Column C does not contain any channel IDs")

    random_offset = random.randrange(channel_count)
    channel_data = sheet_query(
        "select C where C is not null limit 1 offset "
        + str(random_offset)
    )
    channel_cell = channel_data["table"]["rows"][0]["c"][0]
    channel_id = str(channel_cell.get("v", "")).strip() if channel_cell else ""

    if not channel_id:
        raise ValueError("Selected row in column C is empty")

    return channel_id, random_offset


def get_youtube_videos(channel_id, channel_name=""):
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

                "channel":
                    channel_name,

                "url":
                    "https://www.youtube.com/watch?v="
                    + video_id,

            "embed_url":
                "https://www.youtube.com/embed/"
                + video_id
        })

    return videos


def find_matching_channels(search_term):
    sheet_data = sheet_query(
        "select C, D where C is not null and D is not null"
    )
    matching_channels = []

    for row in sheet_data["table"]["rows"]:
        cells = row.get("c") or []
        channel_cell = cells[0] if len(cells) > 0 else None
        name_cell = cells[1] if len(cells) > 1 else None
        channel_id = str(channel_cell.get("v", "")).strip() if channel_cell else ""
        channel_name = str(name_cell.get("v", "")).strip() if name_cell else ""

        if channel_id and search_term.casefold() in channel_name.casefold():
            matching_channels.append((channel_id, channel_name))

    return matching_channels


try:
    search_term = " ".join(sys.argv[1:]).strip()

    if search_term:
        matching_channels = find_matching_channels(search_term)
        videos = []

        for channel_id, channel_name in matching_channels:
            videos.extend(get_youtube_videos(channel_id, channel_name))

        result = {
            "success": True,
            "search_term": search_term,
            "matched_channels": len(matching_channels),
            "videos": videos,
        }
    else:
        channel_id, random_offset = get_random_channel_id()
        videos = get_youtube_videos(channel_id)
        result = {
            "success": True,
            "videos": videos,
            "selected_offset": random_offset,
            "selected_channel_id": channel_id
        }

    print(json.dumps(result))

except Exception as e:

    print(
        json.dumps({
            "success": False,
            "error": str(e)
        })
    )