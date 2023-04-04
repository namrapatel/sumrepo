import requests
import openai
from bs4 import BeautifulSoup
import env
import os.path
import utils

# Initialize OpenAI API
openai.api_key = env.API_KEY

# Define the list of important file extensions
important_extensions = [".py", ".js", ".html", ".css", ".md", ".txt", ".xml", ".json", ".yml", ".yaml", ".ini", ".cfg", ".sh", ".bat", ".ps1", ".php", ".rb", ".java", ".cpp", ".h", ".c", ".cs", ".swift", ".m", ".mm", ".go", ".rs", ".pl", ".pm", ".tcl", ".vhdl", ".verilog", ".asm", ".s", ".tex", ".ts", ".tsx", ".jsx"]


def get_files_in_folder(url, path="", visited_urls=set()):
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
            file_path = path + url.split("/")[-1]
            file_info = {
                "name": url.split("/")[-1],
                "path": file_path,
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
                and href not in visited_urls):
            visited_urls.add(href)
            hrefs.append(href)
            file_infos += get_files_in_folder("https://github.com" + href, path + href.split("/")[-1] + "/", visited_urls)
    return file_infos


# Get the repository URL from user input
repo_url = input("Enter the repository URL: ")

# Extract the repository owner and name from the URL
repo_owner = repo_url.split("/")[-2]
repo_name = repo_url.split("/")[-1]

print("Retrieving files from " + repo_owner + "/" + repo_name + "...")
# Retrieve Github repository contents
url = "https://github.com/" + repo_owner + "/" + repo_name
response = requests.get(url)
soup = BeautifulSoup(response.text, "lxml")

# Extract names and URLs of all files and directories
file_infos = []
for link in soup.find_all("a"):
    href = link.get("href")
    if ((href.startswith("/" + repo_owner + "/" + repo_name + "/tree/master/") or href.startswith("/" + repo_owner + "/" + repo_name + "/blob/master/") or href.startswith("/" + repo_owner + "/" + repo_name + "/tree/main/")) 
            and not href.endswith("/")):
        file_infos += get_files_in_folder("https://github.com" + href)

with open("output.txt", "a") as f:
    f.write("FILE INFOS:\n")
    for file_info in file_infos:
        f.write(str(file_info) + "\n")


# Summarize the contents of each file
summaries = []
for file_info in file_infos:
    print("Summarizing " + file_info["name"] + "...")

    summary = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant who is also an expert Software Engineer. You will be given some code and are asked to summarize its functionality and significance in the codebase that it comes from in 2 sentences or less."},
            {"role": "user", "content": file_info["content"]},
        ],
    )
    print(summary)
    print(summary["choices"][0]["message"])
    summaries.append(summary)

# Write the summaries to a file
with open("output.txt", "a") as f:
    for summary in summaries:
        f.write(summary["choices"][0]["message"] + "\n")