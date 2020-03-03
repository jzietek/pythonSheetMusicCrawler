from urllib.request import urlopen, Request


def get_page_html(url):
    req = prepare_request(url)
    return urlopen(req).read().decode("utf-8")


def prepare_request(req_url):
    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
    return Request(url=req_url, headers=headers)