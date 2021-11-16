"""
Recursive URL crawler, navigate links in a depth-first manner, saving the
title and URL of each link touched. Sets a maximum depth to avoid... problems
"""

from crawler import Crawler, URLFilter
from tree_utils import save_tree_json


if __name__ == '__main__':
    crawler = Crawler(
        head_url='https://docs.python.org',
        branching=1,
        max_depth=15,
        url_filter=URLFilter('python.org', True)
    )
    crawler.crawl()

    save_tree_json(crawler.tree, './saved_crawls/')
    print(f"URL crawl complete! Visited {len(crawler.visited_urls)} pages.")
