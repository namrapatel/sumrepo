import requests
import openai
from bs4 import BeautifulSoup
import env

# Initialize OpenAI API
openai.api_key = env.API_KEY

# Retrieve Github repository contents
url = "https://github.com/HaliteChallenge/Halite"
response = requests.get(url)
soup = BeautifulSoup(response.text, "lxml")

# Extract names and URLs of all files and directories
file_urls = []
for link in soup.find_all("a"):
    href = link.get("href")
    if href.startswith("/HaliteChallenge/Halite/tree/master/"):
        file_urls.append("https://github.com" + href)

# Summarize the contents of each file
summaries = []
print(file_urls)
for file_url in file_urls:
    response = requests.get(file_url)
    text = response.text
    summary = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Who won the world series in 2020?"},
            {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
            {"role": "user", "content": "Where was it played?"}
        ],
    )
    print(summary)