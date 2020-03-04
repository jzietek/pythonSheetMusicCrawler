from urllib.request import urlopen, Request
import os

def get_page_html(url):
    req = prepare_request(url)
    return urlopen(req).read().decode("utf-8")


def prepare_request(req_url):
    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
    return Request(url=req_url, headers=headers)


def remove_bad_characters(path):
    delete_chars = R'<>\/:*?"|'
    for c in delete_chars:
        path = path.replace(c,'')
    return path


def download_file(url, file_path):
    try:
        response = urlopen(url)
        with open(file_path, 'wb') as f:
            f.write(response.read())
        print(F"Downloaded: {file_path}")
    except Exception as err:
        print(F"Exception when downloading {url} to {file_path}: {err}")
