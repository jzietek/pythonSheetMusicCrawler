from html.parser import HTMLParser
from urllib.request import urlopen, Request
from urllib import parse

from main_page_parser import MainPageParser
from index_page_parser import IndexPageParser
from sheet_page_parser import SheetPageParser
from download_page_parser import DownloadPageParser
from utils import prepare_request
from utils import get_page_html

    
def crawl_all(base_url):
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
            google_drive_link = dpp.get_google_drive_link(download_page_link, download_page_html)
            #print(google_drive_link)
            #download_pdf("pdf.pdf") TODO here



    # for link in indexLinks:
    #     #iterate over all 
    #     content_links = get_index_content_links(link)
    #     for content_link in content_links:
    #         read_more_page_link = get_read_more_page_link(content_link)
    #         binary_pdf = get_free_download(read_more_page_link)
    #         save_pdf_to_file(binary_pdf)
    #iterate the link

if __name__ == "__main__":
    crawl_all("https://sheetmusic-free.com/")   
    print("END")
