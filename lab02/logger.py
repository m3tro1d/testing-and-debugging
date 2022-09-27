from datetime import datetime


DATE_FORMAT = '%Y-%m-%d %H:%M'


class Logger:
    def __init__(self, valid_links_filename: str, invalid_links_filename: str):
        self._valid_links_file = open(valid_links_filename, 'w')
        self._invalid_links_file = open(invalid_links_filename, 'w')

    def __del__(self):
        self._valid_links_file.close()
        self._invalid_links_file.close()

    def write_headers(self, domain: str):
        print('valid links for {}\n'.format(domain), file=self._valid_links_file)
        print('invalid links for {}\n'.format(domain), file=self._invalid_links_file)

    def log_valid(self, link):
        print('/' + link.path, file=self._valid_links_file)

    def log_invalid(self, link, status: int):
        print('/{} - {}'.format(link.path, status), file=self._invalid_links_file)

    def write_footers(self, valid_count: int, invalid_count: int):
        timestamp = datetime.now().strftime(DATE_FORMAT)
        print('\ntotal: {}\ntimestamp: {}'.format(valid_count, timestamp), file=self._valid_links_file)
        print('\ntotal: {}\ntimestamp: {}'.format(invalid_count, timestamp), file=self._invalid_links_file)
