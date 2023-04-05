import requests
from bs4 import BeautifulSoup
import utils

important_extensions = [".py", ".js", ".html", ".css", ".md", ".txt", ".xml", ".json", ".yml", ".yaml", ".ini", ".cfg", ".sh", ".bat", ".ps1", ".php", ".rb", ".java", ".cpp", ".h", ".c", ".cs", ".swift", ".m", ".mm", ".go", ".rs", ".pl", ".pm", ".tcl", ".vhdl", ".verilog", ".asm", ".s", ".tex", ".ts", ".tsx", ".jsx"]

def get_soup(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    return soup


def get_files_in_folder(url, repo_owner, repo_name, path="", visited_urls=set()):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")

    # Check if the URL is a file or a folder
    if "." in url.split("/")[-1]:
        # Get the code/text from the file and store the path
        extension = utils.clean_string(url.split(".")[-1]).strip()
        if extension in important_extensions:
            raw_url = utils.transform_url(url).replace("/blob/", "/")
            response = requests.get(raw_url)
            if len(response.content) > 2_000_000:
                print("Skipping file due to large size: " + url)
                return []
            text = response.text
            file_info = {
                "name": url.split("/")[-1],
                "url": raw_url,
                "content": text,
            }
            return [file_info]

    # If the URL is a folder, recursively retrieve all file URLs within it
    file_infos = []
    hrefs = []
    for link in soup.find_all("a"):
        href = link.get("href")
        if ((href.startswith("/" + repo_owner + "/" + repo_name + "/tree/master/") or href.startswith("/" + repo_owner + "/" + repo_name + "/blob/master/") or href.startswith("/" + repo_owner + "/" + repo_name + "/tree/main/") or href.startswith("/" + repo_owner + "/" + repo_name + "/blob/main/")) 
                and not href.endswith("/") 
                and href not in visited_urls
                and href.split("/")[-1] not in IGNORED_FILENAMES):
            visited_urls.add(href)
            hrefs.append(href)
            file_infos += get_files_in_folder("https://github.com" + href, repo_owner, repo_name, path + href.split("/")[-1] + "/", visited_urls)
    return file_infos

# Define a list of ignored file and folder names
IGNORED_FILENAMES = ['.DS_Store', '.git', '.svn', '__pycache__', 'node_modules', 'vendor', '.idea', '.vscode', '.gradle', '.sass-cache']
