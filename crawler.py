from bs4 import BeautifulSoup
import requests
import re
import random

from tree import Tree, TreeNode

from typing import Iterable
Strings = Iterable[str]


class URLFilter:
    """Configurable url filter used by Crawler class"""
    def __init__(
            self,
            query='',
            skip_visited=False
    ):
        self.query: str = query
        self.skip_visited: bool = skip_visited

    def filter(self, urls: Strings, skip_urls: Strings = None) -> list:
        if self.query:
            urls = [url for url in urls if self.query in url]
        if self.skip_visited and skip_urls:
            urls = [url for url in urls if url not in skip_urls]

        return urls


class Crawler:
    def __init__(
            self,
            head_url: str,
            branching: int,
            max_depth: int,
            url_filter: URLFilter = None
    ):
        self.head_url = head_url
        self.visited_urls = set()
        self.tree = Tree(branching, max_depth)

        if url_filter:
            self.url_filter = url_filter  # custom filter
        else:
            self.url_filter = URLFilter()  # null filter

    def crawl(self, url=None, parent_node=None):
        if url is None:
            url = self.head_url

        self.visited_urls.add(url)

        # try except gross
        try:
            soup = self.make_soup(url)
        except Exception as e:
            print(e)
            return -1

        urls: list[str] = self.scrape_urls(soup)
        title: str = self.scrape_title(soup)

        if urls:
            # filter urls
            urls = self.url_filter.filter(urls, self.visited_urls)
            # sample some urls (branching factor)
            urls = random.sample(urls, k=min(self.tree.branching, len(urls)))

        # create node for this page
        new_node: TreeNode
        if not parent_node:
            new_node = self.tree.add_head_node(title, url)
        else:
            new_node = self.tree.add_child_node(title, url, parent_node)

        # recursively crawl a random sample of the urls
        if new_node.depth < self.tree.max_depth:
            for url in urls:
                self.crawl(url, parent_node=new_node)

    def change_filter(self, url_filter: URLFilter) -> None:
        self.url_filter = url_filter

    @staticmethod
    def make_soup(http_link) -> BeautifulSoup:
        # load html and parse in bs4
        r = requests.get(http_link)
        return BeautifulSoup(r.text, 'html.parser')

    @staticmethod
    def scrape_title(soup: BeautifulSoup) -> str:
        title_tag = soup.find('title')
        if title_tag and (title := title_tag.text):
            return title
        else:
            return '*NO_TITLE*'

    @staticmethod
    def scrape_urls(soup: BeautifulSoup) -> list[str]:
        # return all of the links on the page that begin with http or https
        urls = []

        for a_tag in soup.find_all('a'):
            href: str = a_tag.get('href', '')
            if match := re.search(r"^(http|https)://", href):
                urls.append(match.string)
        return urls
