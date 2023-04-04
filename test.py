# import os

url = "https://github.com/HaliteChallenge/Halite/blob/master/admin/cron/"

# if os.path.basename(url).find('.') != -1:
#     print("File found: " + url)

import requests
import openai
from bs4 import BeautifulSoup
import env



def get_all_file_urls(url):
    response = requests.get("https://github.com/HaliteChallenge/Halite/blob/master/admin/cron/")
    soup = BeautifulSoup(response.text, "lxml")
    file_urls = []
    for link in soup.find_all("a"):
        href = link.get("href")
        print(href)
        if href.startswith("/HaliteChallenge/Halite/blob/master/") and not href.endswith("/"):
            with open("output.txt", "a") as f:
                f.write("Main URL: " + url + "\n")
                f.write("Entered sub-URL: " + href + "\n")
            # file_urls += get_files_in_folder("https://github.com" + href)
    return file_urls

# Retrieve Github repository contents
url = "https://github.com/HaliteChallenge/Halite"

file_urls = get_all_file_urls(url)