import requests
import openai
from bs4 import BeautifulSoup
import env

# Initialize OpenAI API
openai.api_key = env.API_KEY

important_extensions = [".py", ".js", ".html", ".md", ".txt", ".xml", ".json", ".yml", ".yaml", ".ini", ".cfg", ".sh", ".bat", ".ps1", ".php", ".rb", ".java", ".cpp", ".h", ".c", ".cs", ".swift", ".m", ".mm", ".go", ".rs", ".pl", ".pm", ".tcl", ".vhdl", ".verilog", ".asm", ".s", ".tex"]

def get_files_in_folder(url, path="", visited_urls=set()):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")

    # Check if the URL is a file or a folder
    if "." in url.split("/")[-1]:
        # Get the code/text from the file and store the path
        extension = url.split(".")[-1]
        if extension in important_extensions:
            response = requests.get(url)
            if len(response.content) > 2_000_000:
                print("Skipping file due to large size: " + url)
                return []
            print("File found: " + url)
            text = response.text
            file_path = path + url.split("/")[-1]
            file_info = {
                "name": url.split("/")[-1],
                "path": file_path,
                "content": text,
            }
            with open("output.txt", "a") as f:
                f.write("File found: " + url + "\n")
                f.write("File path: " + file_path + "\n")
            return [file_info]

    # If the URL is a folder, recursively retrieve all file URLs within it
    file_infos = []
    hrefs = []
    for link in soup.find_all("a"):
        href = link.get("href")
        if ((href.startswith("/HaliteChallenge/Halite/tree/master/") or href.startswith("/HaliteChallenge/Halite/blob/master/")) 
                and not href.endswith("/") 
                and href not in visited_urls):
            visited_urls.add(href)
            with open("output.txt", "a") as f:
                f.write("Entered sub-URL: " + href + "\n")
            hrefs.append(href)
            file_infos += get_files_in_folder("https://github.com" + href, path + href.split("/")[-1] + "/", visited_urls)
    with open("output.txt", "a") as f:
        f.write("Sub-URL: " + url + "\n")
        f.write("Hrefs: " + str(hrefs) + "\n")
    return file_infos


def get_all_file_urls(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    file_urls = []
    for link in soup.find_all("a"):
        href = link.get("href")
        if ((href.startswith("/HaliteChallenge/Halite/tree/master/") or href.startswith("/HaliteChallenge/Halite/blob/master/")) and not href.endswith("/")):
            with open("output.txt", "a") as f:
                f.write("Main URL: " + url + "\n")
                f.write("Entered sub-URL: " + href + "\n")
            file_urls += get_files_in_folder("https://github.com" + href)
    return file_urls

# Retrieve Github repository contents
url = "https://github.com/HaliteChallenge/Halite"
file_urls = get_all_file_urls(url)

with open("output.txt", "a") as f:
    f.write("FILE URLS:\n")
    for file_url in file_urls:
        f.write(str(file_url) + "\n")


# Summarize the contents of each file
# summaries = []
# print(file_urls)
# for file_url in file_urls:
#     response = requests.get(file_url)
#     text = response.text
#     summary = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "You are a helpful assistant."},
#             {"role": "user",
