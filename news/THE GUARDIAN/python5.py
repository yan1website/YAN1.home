import requests
import xml.etree.ElementTree as ET
import json
import re
import html


# ==================================================
# THE GUARDIAN RSS
# ==================================================

RSS_URL = "https://www.theguardian.com/business/rss"


# ==================================================
# GET RSS
# ==================================================

response = requests.get(
    RSS_URL,
    headers={
        "User-Agent": "Mozilla/5.0"
    },
    timeout=20
)

response.raise_for_status()


# ==================================================
# PARSE XML
# ==================================================

root = ET.fromstring(response.content)


# ==================================================
# NAMESPACES
# ==================================================

MEDIA_NS = "{http://search.yahoo.com/mrss/}"


articles = []


# ==================================================
# READ ARTICLES
# ==================================================

for item in root.findall(".//item"):

    title = item.findtext(
        "title",
        ""
    ).strip()


    link = item.findtext(
        "link",
        ""
    ).strip()


    description = item.findtext(
        "description",
        ""
    ).strip()


    published = item.findtext(
        "pubDate",
        ""
    ).strip()


    image_url = ""


    # ----------------------------------------------
    # Try media:content
    # ----------------------------------------------

    media_content = item.find(
        MEDIA_NS + "content"
    )

    if media_content is not None:

        image_url = media_content.get(
            "url",
            ""
        )


    # ----------------------------------------------
    # Try media:thumbnail
    # ----------------------------------------------

    if not image_url:

        thumbnail = item.find(
            MEDIA_NS + "thumbnail"
        )

        if thumbnail is not None:

            image_url = thumbnail.get(
                "url",
                ""
            )


    # ----------------------------------------------
    # Try enclosure
    # ----------------------------------------------

    if not image_url:

        enclosure = item.find(
            "enclosure"
        )

        if enclosure is not None:

            enclosure_type = enclosure.get(
                "type",
                ""
            )

            if enclosure_type.startswith("image"):

                image_url = enclosure.get(
                    "url",
                    ""
                )


    # ----------------------------------------------
    # Clean description
    # ----------------------------------------------

    description = html.unescape(
        description
    )


    description = re.sub(
        r"<[^>]+>",
        "",
        description
    ).strip()


    # ----------------------------------------------
    # Add article
    # ----------------------------------------------

    articles.append({

        "source": "The Guardian",

        "title": title,

        "link": link,

        "description": description,

        "published": published,

        "image": image_url

    })


# ==================================================
# RETURN JSON
# ==================================================

print(
    json.dumps(
        articles,
        ensure_ascii=False
    )
)