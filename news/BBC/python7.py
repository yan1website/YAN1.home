import requests
import feedparser
import json


def getBBCNews():

    try:

        response = requests.get(
        "https://feeds.bbci.co.uk/news/health/rss.xml"
        )

        response.raise_for_status()


        feed = feedparser.parse(
            response.content
        )


        news = []


        for item in feed.entries:

            image = ""


            # media:thumbnail
            if hasattr(item, "media_thumbnail"):

                thumbnails = item.media_thumbnail

                if thumbnails and "url" in thumbnails[0]:

                    image = thumbnails[0]["url"]


            # media:content
            elif hasattr(item, "media_content"):

                media = item.media_content

                if media and "url" in media[0]:

                    image = media[0]["url"]


            # enclosure
            elif hasattr(item, "enclosures"):

                enclosures = item.enclosures

                if enclosures and "href" in enclosures[0]:

                    image = enclosures[0]["href"]


                elif enclosures and "url" in enclosures[0]:

                    image = enclosures[0]["url"]


            news.append({

                "title": getattr(
                    item,
                    "title",
                    ""
                ),

                "link": getattr(
                    item,
                    "link",
                    ""
                ),

                "description": getattr(
                    item,
                    "summary",
                    ""
                ),

                "date": getattr(
                    item,
                    "published",
                    ""
                ),

                "image": image

            })


        print(
            json.dumps(
                news,
                indent=2,
                ensure_ascii=False
            )
        )


    except Exception as error:

        print(
            "Error: " + str(error)
        )


getBBCNews()