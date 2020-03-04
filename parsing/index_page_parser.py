from parsing.page_parser import PageParser

class IndexPageParser(PageParser):

    def handle_endtag(self, tag):
        if tag == "tbody":
            self._in_table = False

    def handle_starttag(self, tag, attrs):
        if tag == "tbody":
            self._in_table = True

        if self._in_table == True and tag == 'a':
            for (key, value) in attrs:
                if key == 'href':
                    self.append_to_links(value)

    def parse(self, page_url, page_html):
        self._in_table = False
        super(IndexPageParser, self).parse(page_url, page_html)

    def get_sheet_page_links(self):
        return self._links