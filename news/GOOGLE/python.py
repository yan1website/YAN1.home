import requests
import xml.etree.ElementTree as ET
import json
import html
import re
import random
from urllib.parse import quote_plus


SEARCH_QUERY = ""
SELECTED_FEED_URL = ""


NEWS_FEED_URLS = [
    "https://news.google.com/rss",
    "https://news.google.com/rss/search?q=technology",
    "https://news.google.com/rss/search?q=artificial+intelligence",
    "https://news.google.com/rss/search?q=health",
    "https://news.google.com/rss/search?q=sports",
    "https://news.google.com/rss/search?q=cricket",
    "https://news.google.com/rss/search?q=football",
    "https://news.google.com/rss/search?q=India",
    "https://news.google.com/rss/search?q=world+news",
    "https://news.google.com/rss/search?q=business",
    "https://news.google.com/rss/search?q=stock+market",
    "https://news.google.com/rss/search?q=economy",
    "https://news.google.com/rss/search?q=gaming",
    "https://news.google.com/rss/search?q=science",
    "https://news.google.com/rss/search?q=space",
    "https://news.google.com/rss/search?q=movies",
    "https://news.google.com/rss/search?q=entertainment",
    "https://news.google.com/rss/search?q=music",
    "https://news.google.com/rss/search?q=gadgets",
    "https://news.google.com/rss/search?q=cybersecurity",
    "https://news.google.com/rss/search?q=programming",
    "https://news.google.com/rss/search?q=web+development",
    "https://news.google.com/rss/search?q=cryptocurrency",
    "https://news.google.com/rss/search?q=politics",
    "https://news.google.com/rss/search?q=education",
    "https://news.google.com/rss/search?q=automobiles",
    "https://news.google.com/rss/search?q=travel",
    "https://news.google.com/rss/search?q=food",
    "https://news.google.com/rss/search?q=lifestyle",
    "https://news.google.com/rss/search?q=environment",
    "https://news.google.com/rss/search?q=weather",
    "https://news.google.com/rss/search?q=jobs+careers",
    "https://news.google.com/rss/search?q=television"
]

if SELECTED_FEED_URL:
    RSS_URLS = [SELECTED_FEED_URL]
elif SEARCH_QUERY.strip():
    RSS_URLS = [
        "https://news.google.com/rss/search?q=" +
        quote_plus(SEARCH_QUERY.strip())
    ]
else:
    RSS_URLS = [random.choice(NEWS_FEED_URLS)]


# ============================================================
# HEADERS
# ============================================================

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/rss+xml, application/xml, text/xml, */*"
}


# ============================================================
# CLEAN HTML
# ============================================================

def clean_text(text):

    if not text:
        return ""

    text = html.unescape(text)

    text = re.sub(
        r"<br\s*/?>",
        "\n",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"<[^>]+>",
        "",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# FIND IMAGE
# ============================================================

def get_image(description, item=None):

    if description:

        description = html.unescape(description)

        match = re.search(
            r'<img[^>]+src=["\']([^"\']+)["\']',
            description,
            re.IGNORECASE
        )

        if match:
            return match.group(1)

        match = re.search(
            r'https?://[^\s"<>]+\.(?:jpg|jpeg|png|gif|webp)(?:\?[^\s"<>]*)?',
            description,
            re.IGNORECASE
        )

        if match:
            return match.group(0)

    if item is not None:

        for element in item.iter():

            element_name = element.tag.rsplit("}", 1)[-1].lower()

            if element_name in ("content", "thumbnail", "enclosure"):

                for attribute_name in ("url", "href"):

                    image_url = element.attrib.get(
                        attribute_name,
                        ""
                    )

                    if image_url.startswith("http"):
                        return image_url
    description = html.unescape(description)


# ============================================================
# GET ONE RSS FEED
# ============================================================

def get_google_news(rss_url):

    articles = []

    try:

        response = requests.get(
            rss_url,
            headers=HEADERS,
            timeout=10
        )

        if response.status_code != 200:

            return [], {
                "url": rss_url,
                "status": response.status_code,
                "error": "HTTP request failed"
            }

        root = ET.fromstring(
            response.content
        )

        channel = root.find("channel")

        if channel is None:

            return [], {
                "url": rss_url,
                "error": "RSS channel not found"
            }

        for item in channel.findall("item"):

            title_element = item.find("title")
            link_element = item.find("link")
            description_element = item.find("description")
            pubdate_element = item.find("pubDate")
            source_element = item.find("source")

            title = (
                title_element.text or ""
                if title_element is not None
                else ""
            )

            link = (
                link_element.text or ""
                if link_element is not None
                else ""
            )

            description = (
                description_element.text or ""
                if description_element is not None
                else ""
            )

            pubdate = (
                pubdate_element.text or ""
                if pubdate_element is not None
                else ""
            )

            source = (
                source_element.text or ""
                if source_element is not None
                else ""
            )

            article = {

                "title": title.strip(),

                "description": clean_text(
                    description
                ),

                "url": link.strip(),

                "source": source.strip(),

                "published": pubdate.strip(),

                "image_url": get_image(
                    description,
                    item
                )
            }

            articles.append(article)

    except Exception as e:

        return [], {
            "url": rss_url,
            "error": str(e)
        }

    return articles, None


# ============================================================
# MAKE ONLY 2 REQUESTS
# ============================================================

all_articles = []
errors = []

for rss_url in RSS_URLS:

    articles, error = get_google_news(
        rss_url
    )

    all_articles.extend(
        articles
    )

    if error:
        errors.append(
            error
        )


# ============================================================
# REMOVE DUPLICATES
# ============================================================

unique_articles = []
seen_urls = set()

for article in all_articles:

    url = article.get(
        "url",
        ""
    )

    if url and url not in seen_urls:

        seen_urls.add(
            url
        )

        unique_articles.append(
            article
        )


# ============================================================
# FINAL JSON
# ============================================================

result = {

    "success": True,

    "source":
        "Google News RSS",

    "requests_made":
        len(RSS_URLS),

    "count":
        len(unique_articles),

    "articles":
        unique_articles,

    "errors":
        errors
}


# ============================================================
# SEND JSON
# ============================================================

print(
    json.dumps(
        result,
        ensure_ascii=False
    )
)