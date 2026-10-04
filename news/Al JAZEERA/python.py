import requests
import xml.etree.ElementTree as ET
import json

RSS_URL = "https://www.aljazeera.com/xml/rss/all.xml"

response = requests.get(
    RSS_URL,
    headers={
        "User-Agent": "Mozilla/5.0"
    },
    timeout=20
)

response.raise_for_status()

root = ET.fromstring(response.content)

# RSS media namespace
media = "{http://search.yahoo.com/mrss/}"

articles = []

for item in root.findall(".//item"):

    image_url = ""

    # Try media:content
    media_content = item.find(media + "content")

    if media_content is not None:
        image_url = media_content.get("url", "")

    # Try media:thumbnail if no content image
    if not image_url:

        thumbnail = item.find(media + "thumbnail")

        if thumbnail is not None:
            image_url = thumbnail.get("url", "")


    articles.append({

        "title": item.findtext("title", ""),

        "link": item.findtext("link", ""),

        "description": item.findtext(
            "description",
            ""
        ),

        "published": item.findtext(
            "pubDate",
            ""
        ),

        "image": image_url

    })


print(
    json.dumps(
        articles,
        ensure_ascii=False
    )
)