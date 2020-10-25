import xml.etree.ElementTree as ElementTree

import requests

google_news_url = "https://news.google.com/news/rss"


def get_headlines(rss_url):
    """
    @returns a list of titles from the rss feed located at `rss_url`    
    """

    resp = requests.get(rss_url)

    feed_tree = ElementTree.fromstring(resp.content)

    return [item.text for item in feed_tree.findall('.//channel/item/title')]


print(get_headlines(google_news_url))
