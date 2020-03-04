from parsing.page_parser import PageParser

class SheetPageParser(PageParser):

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (key, value) in attrs:
                if key == 'href':
                    self.append_to_links(value)


    def handle_data(self, data):
        if data.find("Read more . . .") >= 0:
            self._result = self._links[-1]


    def parse(self, page_url, page_html):
        self._result = ""
        super(SheetPageParser, self).parse(page_url, page_html)


    def get_download_page_link(self):
        return self._result