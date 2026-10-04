import requests
import feedparser
import json


def get_image_url(item):

    for media in item.get("media_content", []):

        image_url = media.get("url", "")

        if image_url:
            return image_url

    for thumbnail in item.get("media_thumbnail", []):

        image_url = thumbnail.get("url", "")

        if image_url:
            return image_url

    for enclosure in item.get("enclosures", []):

        if enclosure.get("type", "").startswith("image/"):
            image_url = enclosure.get("href", enclosure.get("url", ""))

            if image_url:
                return image_url

    return ""


def getNDTVNews():

    url = "https://feeds.feedburner.com/ndtvnews-top-stories"

    try:

        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        response.raise_for_status()

        feed = feedparser.parse(response.content)

        news = []

        for item in feed.entries[:20]:

            news.append({
                "title": item.get("title", ""),
                "description": item.get("summary", ""),
                "link": item.get("link", ""),
                "published": item.get("published", ""),
                "image": get_image_url(item)
            })

        return json.dumps(
            {
                "source": "NDTV",
                "count": len(news),
                "news": news
            },
            ensure_ascii=False
        )

    except Exception as e:

        return json.dumps({
            "source": "NDTV",
            "error": str(e)
        })


print(getNDTVNews())