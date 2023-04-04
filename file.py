import requests
import utils

def get_file_content(url):
    if not url.startswith('http'):
        url = 'https://' + url
    raw_url = utils.transform_url(url).replace("/blob/", "/")
    response = requests.get(raw_url)
    text = response.text
    return text

