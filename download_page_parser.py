from html.parser import HTMLParser
from urllib.request import urlopen, Request
from urllib import parse

class DownloadPageParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
            

    def handle_starttag(self, tag, attrs):
        if tag == 'form':
            for (key, value) in attrs:
                if key == 'action' and value.find("export") >= 0:
                    new_url = parse.urljoin(self._base_url, value)
                    self._links = self._links + [new_url]

    def handle_data(self, data):
        if data == '\n':
            return
        if data.find(" Title:") >= 0:
            self._next_is_title = True
            return
        if data.find(" Artist:") >= 0:
            self._next_is_artist = True
            return
        
        if self._next_is_artist:
            self._artist = data
            self._next_is_artist = False
        if self._next_is_title:
            self._title = data
            self._next_is_title = False

    def parse(self, page_url, page_html):
        self._artist = ""
        self._title = ""
        self._next_is_title = False
        self._next_is_artist = False
        self._links = []
        self._base_url = page_url
        self.feed(page_html)

    def get_parsed_google_drive_link(self):
        if len(self._links) == 0:
            return ""
        return self._links[-1]

    def get_parsed_artist(self):
        return self._artist

    def get_parsed_title(self):
        return self._title