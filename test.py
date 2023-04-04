import requests
from bs4 import BeautifulSoup

url = 'https://raw.githubusercontent.com/HaliteChallenge/Halite/master/admin/cron/haliteEmailer.py'
response = requests.get(url).content
# soup = BeautifulSoup(response.text, 'html.parser')
# code = soup.find('div', {'class': 'highlight'}).text
print(response)



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

# file_urls = get_all_file_urls(url)