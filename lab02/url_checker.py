from bs4 import BeautifulSoup
from datetime import datetime
from dataclasses import dataclass
from queue import Queue
from urllib.parse import urlparse
import requests


DATE_FORMAT = '%Y-%m-%d %H:%M'


@dataclass
class LinkInfo:
    path: str
    full_url: str


class UrlChecker:
    def check(self, root_url, valid_output, invalid_output):
        self._url_queue = Queue()
        self._encountered_urls = {}

        self._root_url = root_url
        self._root_parts = urlparse(root_url)._replace(fragment='')
        self._url_queue.put(LinkInfo(self._root_parts.path, root_url))

        self.write_file_headers(valid_output, invalid_output)

        self._valid_urls_count = 0
        self._invalid_urls_count = 0
        while not self._url_queue.empty():
            url = self._url_queue.get()

            content, status = self.get_page_content(url.full_url)
            if status != 200:
                self.save_invalid_url(invalid_output, url, status)
                self._invalid_urls_count += 1
                continue
            self.save_valid_url(valid_output, url)
            self._valid_urls_count += 1

            for link in self.find_clickable_links(content):
                if link.full_url not in self._encountered_urls:
                    self._url_queue.put(link)
                    self._encountered_urls[link.full_url] = True

        self.write_file_footers(valid_output, invalid_output)

    def write_file_headers(self, valid_output, invalid_output):
        domain = self._root_parts.netloc
        print('valid links for {}\n'.format(domain), file=valid_output)
        print('invalid links for {}\n'.format(domain), file=invalid_output)

    def get_page_content(self, url):
        response = requests.get(url)
        return response.content, response.status_code

    def save_invalid_url(self, output, url, status):
        print('/{} - {}'.format(url.path, status), file=output)

    def save_valid_url(self, output, url):
        print('/' + url.path, file=output)

    def find_clickable_links(self, page_content):
        soup = BeautifulSoup(page_content, 'html.parser')

        result = []
        for link in soup.find_all('a', href=True):
            path = link['href']
            if self.is_valid_local_url_path(path):
                yield LinkInfo(path, self.build_link(path))

    def is_valid_local_url_path(self, url):
        if url == '#':
            return False

        for method in ('http', 'tel', 'mailto'):
            if method in url:
                return False

        return True

    def build_link(self, link):
        return self._root_parts._replace(path=link).geturl()

    def write_file_footers(self, valid_output, invalid_output):
        timestamp = datetime.now().strftime(DATE_FORMAT)
        print('\ntotal: {}\ntimestamp: {}'.format(self._valid_urls_count, timestamp), file=valid_output)
        print('\ntotal: {}\ntimestamp: {}'.format(self._invalid_urls_count, timestamp), file=invalid_output)
