import requests
import xml.etree.ElementTree as ET
import json
import re
import html
import random


# List of all RSS URLs
RSS_URLS = [
    # 1. General / Everything
    "https://www.reddit.com/r/news+worldnews+politics+technology+science+business+economics+gaming+movies+television+music+books+sports+memes+funny+pics+videos+interestingasfuck+todayilearned+askreddit/new/.rss",
    
    # 2. Technology + Programming
    "https://www.reddit.com/r/technology+programming+webdev+learnprogramming+Python+javascript+reactjs+node+androiddev+Android+linux+windows+apple+cybersecurity+netsec+opensource+devops+Docker+kubernetes+MachineLearning+artificial+ChatGPT+LocalLLaMA/new/.rss",
    
    # 3. News + World
    "https://www.reddit.com/r/news+worldnews+UpliftingNews+geopolitics+internationalnews+politics+worldevents+india+IndianNews+IndiaSpeaks+UnitedStates+europe+asia+MiddleEast+africa+canada+Australia/new/.rss",
    
    # 4. Sports
    "https://www.reddit.com/r/sports+soccer+football+cricket+tennis+nba+nfl+nhl+baseball+formula1+motogp+boxing+MMA+golf+cycling+Olympics+running+Fitness+IndianSports/new/.rss",
    
    # 5. Gaming
    "https://www.reddit.com/r/gaming+Games+pcgaming+PS5+PS4+XboxSeriesX+XboxOne+NintendoSwitch+Steam+GameDeals+Minecraft+Fortnite+Pokemon+GTA+zelda+leagueoflegends+valorant+PUBG+gamingnews/new/.rss",
    
    # 6. Science + Space
    "https://www.reddit.com/r/science+space+NASA+Astronomy+astrophysics+Physics+chemistry+biology+biologymemes+mathematics+geology+environment+climate+ClimateChange+technology+Futurology+AskScience/new/.rss",
    
    # 7. Movies + TV + Entertainment
    "https://www.reddit.com/r/movies+MovieNews+TrueFilm+television+TVShows+netflix+NetflixBestOf+DisneyPlus+HBO+marvel+MarvelStudios+DC_Cinematic+StarWars+anime+AnimeSuggest+bollywood+tollywood+IndianCinema/new/.rss",
    
    # 8. Memes + Funny
    "https://www.reddit.com/r/memes+funny+dankmemes+wholesomememes+me_irl+AdviceAnimals+MemeEconomy+ComedyCemetery+ProgrammerHumor+technicallythetruth+Showerthoughts+Unexpected+interestingasfuck+blursedimages+funnyvideos/new/.rss",
    
    # 9. India
    "https://www.reddit.com/r/india+IndianNews+IndiaSpeaks+indiadiscussion+IndianGaming+Indian_Academia+IndianFood+IndianHistory+IndianSports+bollywood+bollywoodmemes+Cricket+IndianStreetFood+IndiaInvestments+developersIndia+hyderabad+bangalore+Chennai+Mumbai+Delhi+AndhraPradesh/new/.rss",
    
    # 10. AI + ChatGPT
    "https://www.reddit.com/r/ChatGPT+OpenAI+artificial+ArtificialIntelligence+MachineLearning+deeplearning+LocalLLaMA+singularity+LLMDevs+PromptEngineering+stablediffusion+midjourney+ClaudeAI+GeminiAI+MicrosoftCopilot/new/.rss",
    
    # 11. Programming + Developers
    "https://www.reddit.com/r/programming+learnprogramming+AskProgramming+Python+learnpython+javascript+webdev+reactjs+node+typescript+java+cpp+csharp+golang+rust+php+SQL+database+devops+GitHub+opensource/new/.rss",
    
    # 12. Business + Finance
    "https://www.reddit.com/r/business+economics+finance+investing+stocks+StockMarket+wallstreetbets+personalfinance+Entrepreneur+startups+smallbusiness+IndiaInvestments+IndianStockMarket+CryptoCurrency+technology+businessnews/new/.rss",
    
    # 13. Education + Learning
    "https://www.reddit.com/r/education+AskAcademia+college+GradSchool+learnprogramming+learnpython+learnmath+mathematics+Physics+chemistry+biology+AskScience+todayilearned+YouShouldKnow+LifeProTips+GATEtard/new/.rss",
    
    # 14. Huge mixed feed
    "https://www.reddit.com/r/technology+programming+webdev+Python+ChatGPT+artificial+science+space+physics+gaming+pcgaming+movies+television+music+books+sports+soccer+cricket+nba+news+worldnews+india+IndianNews+business+economics+investing+memes+funny+pics+videos+todayilearned+interestingasfuck+AskReddit+LifeProTips+UpliftingNews+Futurology+opensource+linux+android+anime+bollywood/new/.rss",
    
    # 15. Large "news website" style feed
    "https://www.reddit.com/r/news+worldnews+technology+science+business+economics+politics+gaming+sports+soccer+cricket+movies+television+music+sports+education+anime/new/.rss"
]

# Select a random URL from the list
RSS_URL = random.choice(RSS_URLS)


try:

    response = requests.get(
        RSS_URL,
        headers={
            "User-Agent": "YAN1Website/1.0",
            "Accept": "application/rss+xml, application/xml, text/xml, */*"
        },
        timeout=20
    )


    if response.status_code != 200:

        print(json.dumps({
            "success": False,
            "status": response.status_code,
            "error": response.text[:1000]
        }))

    else:

        root = ET.fromstring(response.content)

        posts = []

        namespace = {
            "atom": "http://www.w3.org/2005/Atom",
            "media": "http://search.yahoo.com/mrss/"
        }


        for entry in root.findall(
            "atom:entry",
            namespace
        ):

            # =================================================
            # TITLE
            # =================================================

            title = entry.find(
                "atom:title",
                namespace
            )


            # =================================================
            # REDDIT URL
            # =================================================

            link = entry.find(
                "atom:link",
                namespace
            )


            # =================================================
            # AUTHOR
            # =================================================

            author = entry.find(
                "atom:author/atom:name",
                namespace
            )


            # =================================================
            # PUBLISHED
            # =================================================

            published = entry.find(
                "atom:published",
                namespace
            )


            # =================================================
            # UPDATED
            # =================================================

            updated = entry.find(
                "atom:updated",
                namespace
            )


            # =================================================
            # CONTENT
            # =================================================

            content = entry.find(
                "atom:content",
                namespace
            )


            # =================================================
            # BASIC INFORMATION
            # =================================================

            title_text = (
                title.text
                if title is not None and title.text
                else ""
            )


            reddit_url = (
                link.attrib.get("href", "")
                if link is not None
                else ""
            )


            author_text = (
                author.text
                if author is not None and author.text
                else ""
            )


            published_text = (
                published.text
                if published is not None and published.text
                else ""
            )


            updated_text = (
                updated.text
                if updated is not None and updated.text
                else ""
            )


            # =================================================
            # DESCRIPTION
            # =================================================

            description = ""


            if content is not None:

                description = content.text or ""

                description = html.unescape(
                    description
                )


                # Remove HTML tags

                description = re.sub(
                    r"<br\s*/?>",
                    "\n",
                    description,
                    flags=re.IGNORECASE
                )


                description = re.sub(
                    r"<[^>]+>",
                    "",
                    description
                )


                # Clean whitespace

                description = re.sub(
                    r"\n\s*\n+",
                    "\n\n",
                    description
                )


                description = re.sub(
                    r"[ \t]+",
                    " ",
                    description
                )


                description = description.strip()


            # =================================================
            # IMAGE URL
            # =================================================

            image_url = ""


            # -------------------------------------------------
            # Method 1: media:thumbnail
            # -------------------------------------------------

            thumbnail = entry.find(
                "media:thumbnail",
                namespace
            )


            if thumbnail is not None:

                image_url = thumbnail.attrib.get(
                    "url",
                    ""
                )


            # -------------------------------------------------
            # Method 2: media:content
            # -------------------------------------------------

            if not image_url:

                media_content = entry.find(
                    "media:content",
                    namespace
                )


                if media_content is not None:

                    media_type = media_content.attrib.get(
                        "type",
                        ""
                    )


                    media_url = media_content.attrib.get(
                        "url",
                        ""
                    )


                    if (
                        media_url
                        and
                        (
                            media_type.startswith("image/")
                            or
                            re.search(
                                r"\.(jpg|jpeg|png|gif|webp)(\?|$)",
                                media_url,
                                re.IGNORECASE
                            )
                        )
                    ):

                        image_url = media_url


            # -------------------------------------------------
            # Method 3: image inside content
            # -------------------------------------------------

            if not image_url and content is not None:

                content_text = content.text or ""

                content_text = html.unescape(
                    content_text
                )


                image_match = re.search(
                    r'<img[^>]+src=["\']([^"\']+)["\']',
                    content_text,
                    re.IGNORECASE
                )


                if image_match:

                    image_url = image_match.group(1)


            # -------------------------------------------------
            # Method 4: direct image URL
            # -------------------------------------------------

            if not image_url and content is not None:

                content_text = content.text or ""

                content_text = html.unescape(
                    content_text
                )


                image_match = re.search(
                    r'https?://[^\s"<>]+'
                    r'\.(?:jpg|jpeg|png|gif|webp)'
                    r'(?:\?[^\s"<>]*)?',
                    content_text,
                    re.IGNORECASE
                )


                if image_match:

                    image_url = image_match.group(0)


            # =================================================
            # CREATE POST
            # =================================================

            post = {

                "title": title_text,

                "description": description,

                "url": reddit_url,

                "author": author_text,

                "published": published_text,

                "updated": updated_text,

                "image_url": image_url

            }


            posts.append(post)


        # =====================================================
        # FINAL JSON
        # =====================================================

        result = {

            "success": True,

            "source": "reddit",

            "count": len(posts),

            "posts": posts

        }


        print(
            json.dumps(
                result,
                ensure_ascii=False
            )
        )


except Exception as e:

    print(
        json.dumps({
            "success": False,
            "error": str(e)
        })
    )