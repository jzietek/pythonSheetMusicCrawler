import os
import sys

from parsing.main_page_parser import MainPageParser
from parsing.index_page_parser import IndexPageParser
from parsing.sheet_page_parser import SheetPageParser
from parsing.download_page_parser import DownloadPageParser

from utils import prepare_request
from utils import get_page_html
from utils import download_file
from utils import remove_bad_characters
    
def crawl_all(base_url, output_dir):
    output_dir = os.path.abspath(output_dir)
    if not os.path.isdir(output_dir):
        print(F"Bad output directory path: {output_dir}")
        return
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
        print(F"Created output directory: {output_dir}")
    
    mpp = MainPageParser()
    ipp = IndexPageParser()
    spp = SheetPageParser()
    dpp = DownloadPageParser()

    counter = 0

    main_page_html = get_page_html(base_url)    
    mpp.parse(base_url, main_page_html)
    index_links = mpp.get_index_links()
        
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
            
            try:
                download_file(google_drive_link, file_path)
                print(F"Downloaded: {file_path}")
                counter += 1
            except Exception as err:
                print(F"Exception when downloading {google_drive_link} to {file_path}: {err}")

    print(F"Completed download of {counter} files.")


if __name__ == "__main__":
    url = "https://sheetmusic-free.com/"
    output_dir = "./output"
    if len(sys.argv) > 2:
        url = sys.argv[1]
        output_dir = sys.argv[2]

    crawl_all(url, output_dir)    
    