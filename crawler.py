import os
import sys
import _thread

from parsing.main_page_parser import MainPageParser
from parsing.index_page_parser import IndexPageParser
from parsing.sheet_page_parser import SheetPageParser
from parsing.download_page_parser import DownloadPageParser

from utils import prepare_request
from utils import get_page_html
from utils import download_file
from utils import remove_bad_characters
    

def narrow_search(index_chars, index_links):
    if len(index_chars) == 0:
        return index_links
    
    index_chars = index_chars.replace(",", "")
    result = []
    for link in index_links:
        for c in index_chars:
            if link.endswith(c + "/"): 
                result += [link]
    return result


def crawl_all(base_url, output_dir, index_chars = ""):
    output_dir = os.path.abspath(output_dir)
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
        print(F"Created output directory: {output_dir}")
    
    mpp = MainPageParser()
    ipp = IndexPageParser()
    spp = SheetPageParser()
    dpp = DownloadPageParser()

    main_page_html = get_page_html(base_url)    
    mpp.parse(base_url, main_page_html)
    index_links = mpp.get_index_links()

    index_links = narrow_search(index_chars, index_links)
        
    for index_link in index_links:
        #print(index_link)
        index_page_html = get_page_html(index_link)
        ipp.parse(index_link, index_page_html)
        sheet_page_links = ipp.get_sheet_page_links()


        for sheet_page_link in sheet_page_links:
            #print(sheet_page_link)
            sheet_page_html = get_page_html(sheet_page_link)
        
            spp.parse(sheet_page_link, sheet_page_html)
            download_page_link = spp.get_download_page_link()
            #print(download_page_link)
            download_page_html = get_page_html(download_page_link)
            dpp.parse(download_page_link, download_page_html)

            google_drive_link = dpp.get_parsed_google_drive_link()
            artist = dpp.get_parsed_artist()
            title = dpp.get_parsed_title()
            
            if artist == "" or title == "":
                file_path = F"{sheet_page_link.replace(base_url, '')}.pdf"
            else:
                file_path = F"{artist}_{title}.pdf"
            file_path = remove_bad_characters(file_path)
            file_path = os.path.join(output_dir, file_path)
            
            #_thread.start_new_thread(download_file, (google_drive_link, file_path))
            if not os.path.exists(file_path):
                download_file(google_drive_link, file_path)

    print(F"Completed.")


if __name__ == "__main__":
    url = "https://sheetmusic-free.com/"
    output_dir = "./output"
    index_chars = ""

    if len(sys.argv) > 2:
        url = sys.argv[1]
        output_dir = sys.argv[2]

    if len(sys.argv) > 3:
        index_chars = sys.argv[3]

    crawl_all(url, output_dir, index_chars)    
    