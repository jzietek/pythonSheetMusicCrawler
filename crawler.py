import os

from html.parser import HTMLParser
from urllib.request import urlopen, Request
from urllib import parse

from main_page_parser import MainPageParser
from index_page_parser import IndexPageParser
from sheet_page_parser import SheetPageParser
from download_page_parser import DownloadPageParser
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

    main_page_html = get_page_html(base_url)    
    index_links = mpp.get_index_links(base_url, main_page_html)
        
    for index_link in index_links:
        #print(index_link)
        index_page_html = get_page_html(index_link)
        sheet_page_links = ipp.get_sheet_page_links(index_link, index_page_html)
        for sheet_page_link in sheet_page_links:
            #print(sheet_page_link)
            sheet_page_html = get_page_html(sheet_page_link)
            download_page_link = spp.get_download_page_link(sheet_page_link, sheet_page_html)
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
            except Exception as err:
                print(F"Exception when downloading {google_drive_link} to {file_path}: {err}")

if __name__ == "__main__":
    crawl_all("https://sheetmusic-free.com/", "./output")    
    print("END")
