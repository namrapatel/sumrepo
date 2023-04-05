import string 
import requests

def is_file(url):
    return "." in url.split("/")[-1]

def clean_string(s):
    remove_chars = set(string.ascii_uppercase + string.digits + string.punctuation)

    clean_s = ''.join(c for c in s if c not in remove_chars)
    
    # TODO: Fix this
    return "."+clean_s

def transform_url(url):
    parts = url.split('/')

    parts[2] = 'raw.githubusercontent.com'

    parts[4] = parts[4].replace('blob/', '')

    new_url = '/'.join(parts)

    return new_url

def get_file_content(url):
    if not url.startswith('http'):
        url = 'https://' + url
    raw_url = transform_url(url).replace("/blob/", "/")
    response = requests.get(raw_url)
    text = response.text
    return text

def get_path_from_url(url: str, repo_owner: str) -> str:
    index = url.find(repo_owner)
    if index != -1:
        return url[index:]
    else:
        return url