from html.parser import HTMLParser
from urllib.request import urlopen, Request
from urllib import parse

class SheetPageParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self._result = ""

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (key, value) in attrs:
                if key == 'href':
                    new_url = parse.urljoin(self._base_url, value)
                    self._links = self._links + [new_url]
    

    def handle_data(self, data):
        if data.find("Read more . . .") >= 0:
            self._result = self._links[-1]
        

    def get_download_page_link(self, page_url, page_html):
        self._links = []
        self._base_url = page_url
        self.feed(page_html)
        return self._result