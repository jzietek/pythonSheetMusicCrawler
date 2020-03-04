from parsing.page_parser import PageParser

class MainPageParser(PageParser):

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (key, value) in attrs:
                if key == 'href' and value.find("xstore/index-") > 0:
                    self.append_to_links(value)


    def get_index_links(self):
        return self._links