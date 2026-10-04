import requests
import xml.etree.ElementTree as ET
import json
import html
import re
import random


# ============================================================
# LEMMY RSS URL
# ============================================================

RSS_URLS = {
    "News": [
        "https://lemmy.world/feeds/c/news.xml?sort=New",
        "https://lemmy.world/feeds/c/worldnews.xml?sort=New",
        "https://lemmy.world/feeds/c/india.xml?sort=New",
        "https://lemmy.world/feeds/c/politics.xml?sort=New"
    ],
    "Technology": [
        "https://lemmy.world/feeds/c/technology.xml?sort=New",
        "https://lemmy.world/feeds/c/programming.xml?sort=New",
        "https://lemmy.world/feeds/c/linux.xml?sort=New",
        "https://lemmy.world/feeds/c/selfhosted.xml?sort=New",
        "https://lemmy.world/feeds/c/android.xml?sort=New",
        "https://lemmy.world/feeds/c/opensource.xml?sort=New",
        "https://lemmy.world/feeds/c/fediverse.xml?sort=New"
    ],
    "Gaming": [
        "https://lemmy.world/feeds/c/gaming.xml?sort=New",
        "https://lemmy.world/feeds/c/games.xml?sort=New"
    ],
    "Science & Space": [
        "https://lemmy.world/feeds/c/science.xml?sort=New",
        "https://lemmy.world/feeds/c/space.xml?sort=New",
        "https://lemmy.world/feeds/c/astronomy.xml?sort=New"
    ],
    "Memes & Fun": [
        "https://lemmy.world/feeds/c/memes.xml?sort=New",
        "https://lemmy.world/feeds/c/lemmy_shitpost.xml?sort=New",
        "https://lemmy.world/feeds/c/tech_memes.xml?sort=New",
        "https://lemmy.world/feeds/c/comic_strips.xml?sort=New",
        "https://lemmy.world/feeds/c/politicalmemes.xml?sort=New"
    ],
    "Entertainment": [
        "https://lemmy.world/feeds/c/movies.xml?sort=New",
        "https://lemmy.world/feeds/c/music.xml?sort=New",
        "https://lemmy.world/feeds/c/tv.xml?sort=New",
        "https://lemmy.world/feeds/c/anime.xml?sort=New"
    ],
    "Hobbies & Lifestyle": [
        "https://lemmy.world/feeds/c/photography.xml?sort=New",
        "https://lemmy.world/feeds/c/diy.xml?sort=New",
        "https://lemmy.world/feeds/c/cooking.xml?sort=New",
        "https://lemmy.world/feeds/c/gardening.xml?sort=New",
        "https://lemmy.world/feeds/c/books.xml?sort=New",
        "https://lemmy.world/feeds/c/travel.xml?sort=New"
    ],
    "General": [
        "https://lemmy.world/feeds/c/asklemmy.xml?sort=New",
        "https://lemmy.world/feeds/c/mildlyinfuriating.xml?sort=New",
        "https://lemmy.world/feeds/c/showerthoughts.xml?sort=New",
        "https://lemmy.world/feeds/c/nostupidquestions.xml?sort=New",
        "https://lemmy.world/feeds/c/youshouldknow.xml?sort=New"
    ]
}

ALL_RSS_URL = "https://lemmy.world/feeds/all.xml?sort=New"

# Values are replaced by index.html for each request.
REQUESTED_RSS_URL = ""
SEARCH_TERM = ""


# ============================================================
# HEADERS
# ============================================================

HEADERS = {
    "User-Agent": "YAN1Website/1.0",
    "Accept": "application/rss+xml, application/atom+xml, application/xml, text/xml, */*"
}


# ============================================================
# CLEAN HTML
# ============================================================

def clean_text(text):

    if not text:
        return ""

    text = html.unescape(text)

    # Keep the description text, but do not expose URLs from the feed.
    text = re.sub(
        r"https?://[^\s<>\"']+|www\.[^\s<>\"']+",
        "",
        text,
        flags=re.IGNORECASE
    )

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

def get_image(text):

    if not text:
        return ""

    text = html.unescape(text)

    # <img src="...">
    match = re.search(
        r'<img[^>]+src=["\']([^"\']+)["\']',
        text,
        re.IGNORECASE
    )

    if match:
        return match.group(1)

    # enclosure URL
    match = re.search(
        r'<enclosure[^>]+url=["\']([^"\']+)["\']',
        text,
        re.IGNORECASE
    )

    if match:
        return match.group(1)

    # Direct image URL
    match = re.search(
        r'https?://[^\s"<>]+\.(?:jpg|jpeg|png|gif|webp)(?:\?[^\s"<>]*)?',
        text,
        re.IGNORECASE
    )

    if match:
        return match.group(0)

    return ""


# ============================================================
# GET XML TEXT
# ============================================================

def get_element_text(parent, tag):

    element = parent.find(tag)

    if element is not None:
        return element.text or ""

    return ""


# ============================================================
# GET LEMMY NEWS
# ============================================================

def get_lemmy():

    articles = []
    rss_url = REQUESTED_RSS_URL or random.choice(
        [url for urls in RSS_URLS.values() for url in urls]
    )

    try:

        response = requests.get(
            rss_url,
            headers=HEADERS,
            timeout=15
        )

        if response.status_code != 200:

            return {
                "success": False,
                "status": response.status_code,
                "error": "Lemmy RSS request failed",
                "url": rss_url
            }

        root = ET.fromstring(
            response.content
        )


        # ====================================================
        # RSS
        # ====================================================

        items = root.findall(
            ".//item"
        )


        # ====================================================
        # ATOM
        # ====================================================

        if not items:

            atom_namespace = {
                "atom": "http://www.w3.org/2005/Atom"
            }

            entries = root.findall(
                "atom:entry",
                atom_namespace
            )

        else:

            entries = []


        # ====================================================
        # RSS ITEMS
        # ====================================================

        for item in items:

            title = get_element_text(
                item,
                "title"
            )

            link = get_element_text(
                item,
                "link"
            )

            description = get_element_text(
                item,
                "description"
            )

            published = get_element_text(
                item,
                "pubDate"
            )

            author = get_element_text(
                item,
                "author"
            )

            creator = get_element_text(
                item,
                "{http://purl.org/dc/elements/1.1/}creator"
            )

            if not author:
                author = creator


            # =================================================
            # IMAGE
            # =================================================

            image_url = get_image(
                description
            )


            # =================================================
            # ENCLOSURE
            # =================================================

            enclosure = item.find(
                "enclosure"
            )

            if enclosure is not None:

                enclosure_url = enclosure.attrib.get(
                    "url",
                    ""
                )

                if enclosure_url:
                    image_url = enclosure_url


            # =================================================
            # COMMUNITY
            # =================================================

            community = ""

            category = item.find(
                "category"
            )

            if category is not None:

                community = (
                    category.text or ""
                )


            # =================================================
            # DESCRIPTION
            # =================================================

            clean_description = clean_text(
                description
            )


            article = {

                "title":
                    html.unescape(
                        title
                    ).strip(),

                "description":
                    clean_description,

                "url":
                    link.strip(),

                "source":
                    "Lemmy",

                "author":
                    author.strip(),

                "community":
                    community.strip(),

                "published":
                    published.strip(),

                "image_url":
                    image_url.strip()
            }


            articles.append(
                article
            )


        # ====================================================
        # ATOM ENTRIES
        # ====================================================

        atom_namespace = {
            "atom": "http://www.w3.org/2005/Atom"
        }


        for entry in entries:

            title_element = entry.find(
                "atom:title",
                atom_namespace
            )

            summary_element = entry.find(
                "atom:summary",
                atom_namespace
            )

            content_element = entry.find(
                "atom:content",
                atom_namespace
            )

            published_element = entry.find(
                "atom:published",
                atom_namespace
            )

            author_element = entry.find(
                "atom:author/atom:name",
                atom_namespace
            )


            title = (
                title_element.text or ""
                if title_element is not None
                else ""
            )


            description = ""

            if summary_element is not None:
                description = (
                    summary_element.text or ""
                )

            elif content_element is not None:
                description = (
                    content_element.text or ""
                )


            link = ""

            link_element = entry.find(
                "atom:link",
                atom_namespace
            )

            if link_element is not None:

                link = link_element.attrib.get(
                    "href",
                    ""
                )


            published = (
                published_element.text or ""
                if published_element is not None
                else ""
            )


            author = (
                author_element.text or ""
                if author_element is not None
                else ""
            )


            image_url = get_image(
                description
            )


            article = {

                "title":
                    html.unescape(
                        title
                    ).strip(),

                "description":
                    clean_text(
                        description
                    ),

                "url":
                    link.strip(),

                "source":
                    "Lemmy",

                "author":
                    author.strip(),

                "community":
                    "",

                "published":
                    published.strip(),

                "image_url":
                    image_url.strip()
            }


            articles.append(
                article
            )


        # ====================================================
        # REMOVE DUPLICATES
        # ====================================================

        unique_articles = []

        seen = set()

        for article in articles:

            url = article.get(
                "url",
                ""
            )

            if url and url not in seen:

                seen.add(
                    url
                )

                unique_articles.append(
                    article
                )

        if SEARCH_TERM.strip():
            search_words = SEARCH_TERM.lower().split()
            unique_articles = [
                article for article in unique_articles
                if all(
                    word in " ".join(
                        str(article.get(field, ""))
                        for field in ("title", "description", "community")
                    ).lower()
                    for word in search_words
                )
            ]


        # ====================================================
        # FINAL RESULT
        # ====================================================

        return {

            "success":
                True,

            "source":
                "Lemmy RSS",

            "url":
                rss_url,

            "count":
                len(unique_articles),

            "articles":
                unique_articles
        }


    except Exception as e:

        return {

            "success":
                False,

            "error":
                str(e),

            "url":
                rss_url
        }


# ============================================================
# EXECUTE
# ============================================================

result = get_lemmy()


# ============================================================
# OUTPUT JSON ONLY
# ============================================================

print(
    json.dumps(
        result,
        ensure_ascii=False
    )
)