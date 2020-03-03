from html.parser import HTMLParser
from urllib.request import urlopen, Request
from urllib import parse

class IndexPageParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self._in_table = False

    def handle_endtag(self, tag):
        if tag == "tbody":
            self._in_table = False

    def handle_starttag(self, tag, attrs):
        if tag == "tbody":
            self._in_table = True

        if self._in_table == True and tag == 'a':
            for (key, value) in attrs:
                if key == 'href':
                    new_url = parse.urljoin(self._base_url, value)
                    self._links = self._links + [new_url]      

    def get_sheet_page_links(self, page_url, page_html):
        self._links = []
        self._base_url = page_url
        self.feed(page_html)
        return self._links