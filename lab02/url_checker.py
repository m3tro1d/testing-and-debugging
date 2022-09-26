from bs4 import BeautifulSoup
from queue import Queue
from urllib.parse import urlparse
import requests


class UrlChecker:
    def check(self, root_url, valid_output, invalid_output):
        self._url_queue = Queue()
        self._encountered_urls = {}

        self._root_parts = urlparse(root_url)._replace(fragment='')
        self._url_queue.put(root_url)

        while not self._url_queue.empty():
            url = self._url_queue.get()

            content, status = self.get_page_content(url)
            if status != 200:
                self.save_invalid_url(invalid_output, url, status)
                continue
            self.save_valid_url(valid_output, url)

            for link in self.find_clickable_links(content):
                if link not in self._encountered_urls:
                    self._url_queue.put(link)
                    self._encountered_urls[link] = True

    def get_page_content(self, url):
        response = requests.get(url)
        return response.content, response.status_code

    def save_invalid_url(self, output, url, status):
        print('{}: {}'.format(status, url), file=output)

    def save_valid_url(self, output, url):
        print(url, file=output)

    def find_clickable_links(self, page_content):
        soup = BeautifulSoup(page_content, 'html.parser')

        result = []
        for link in soup.find_all('a', href=True):
            if self.is_valid_local_url(link['href']):
                yield self.build_link(link['href'])

    def is_valid_local_url(self, url):
        if url == '#':
            return False

        for method in ('http', 'tel', 'mailto'):
            if method in url:
                return False

        return True

    def build_link(self, link):
        return self._root_parts._replace(path=link).geturl()
