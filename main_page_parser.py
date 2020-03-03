from html.parser import HTMLParser
from urllib.request import urlopen, Request
from urllib import parse

class MainPageParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)


    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (key, value) in attrs:
                if key == 'href' and value.find("xstore/index-") > 0:
                    new_url = parse.urljoin(self._base_url, value)
                    self._links = self._links + [new_url]      


    def get_index_links(self, page_url, page_html):
        self._links = []
        self._base_url = page_url
        self.feed(page_html)
        return self._links