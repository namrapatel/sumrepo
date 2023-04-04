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
        print("extension: "+extension)
        if extension in important_extensions:
            raw_url = utils.transform_url(url).replace("/blob/", "/")
            print("raw: "+raw_url)
            response = requests.get(raw_url)
            print("response: \n")
            print(response)
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
        if ((href.startswith("/" + repo_owner + "/" + repo_name + "/tree/master/") or href.startswith("/" + repo_owner + "/" + repo_name + "/blob/master/") or href.startswith("/" + repo_owner + "/" + repo_name + "/tree/main/") or href.startswith("/" + repo_owner + "/" + repo_name + "/blob/main/")) 
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
        with open("output.txt", "a") as f:
            f.write("Main URL: " + url + "\n")
            f.write("Entered subURL " + href + "\n")
            file_infos += get_files_in_folder("https://github.com" + href)

with open("output.txt", "a") as f:
    f.write("FILE INFOS:\n")
    for file_info in file_infos:
        f.write(str(file_info) + "\n")

# Save the file contents to disk
for file_info in file_infos:
    file_path = file_info["path"]
    file_content = file_info["content"]
    dir_path = os.path.dirname(file_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    with open(file_path, "w") as f:
        f.write(file_content)



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
