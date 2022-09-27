from bs4 import BeautifulSoup
from dataclasses import dataclass
from logger import Logger
from queue import Queue
from urllib.parse import urlparse
import requests


@dataclass
class LinkInfo:
    path: str
    full_url: str


class LinkChecker:
    def __init__(self, logger: Logger):
        self._logger = logger

    def check(self, root_url: str):
        self._root_url = root_url
        self._root_parts = urlparse(root_url)._replace(fragment='')

        self._link_queue = Queue()
        self._encountered_urls = {}
        self._link_queue.put(LinkInfo(self._root_parts.path, root_url))

        self._logger.write_headers(self._root_parts.netloc)

        self._valid_urls_count = 0
        self._invalid_urls_count = 0

        while not self._link_queue.empty():
            link = self._link_queue.get()

            content, status = self.get_page_content(link.full_url)
            if status != 200:
                self._logger.log_invalid(link, status)
                self._invalid_urls_count += 1
                continue
            self._logger.log_valid(link)
            self._valid_urls_count += 1

            for link in self.find_clickable_links(content):
                if link.full_url not in self._encountered_urls:
                    self._link_queue.put(link)
                    self._encountered_urls[link.full_url] = True

        self._logger.write_footers(self._valid_urls_count, self._invalid_urls_count)

    def get_page_content(self, url):
        response = requests.get(url)
        return response.content, response.status_code

    def find_clickable_links(self, page_content):
        soup = BeautifulSoup(page_content, 'html.parser')

        result = []
        for link in soup.find_all('a', href=True):
            path = link['href']
            if self.is_valid_local_url_path(path):
                yield LinkInfo(path, self.build_link(path))

    def is_valid_local_url_path(self, url: str):
        if url == '#':
            return False

        for method in ('http', 'tel', 'mailto'):
            if method in url:
                return False

        return True

    def build_link(self, link):
        return self._root_parts._replace(path=link).geturl()
