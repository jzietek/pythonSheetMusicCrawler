from html.parser import HTMLParser
from urllib import parse

class PageParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self._links = []

    def append_to_links(self, value):
        new_url = parse.urljoin(self._base_url, value)
        self._links = self._links + [new_url]  

    def parse(self, page_url, page_html):
        self._links = []
        self._base_url = page_url
        self.feed(page_html)