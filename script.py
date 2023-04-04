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
    if href.startswith("/HaliteChallenge/Halite/blob/master/"):
        file_urls.append("https://github.com" + href)

# Summarize the contents of each file
summaries = []
print(file_urls)
for file_url in file_urls:
    response = requests.get(file_url)
    text = response.text
    summary = openai.Completion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Who won the world series in 2020?"},
            {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
            {"role": "user", "content": "Where was it played?"}
        ],
        temperature=0.5,
        max_tokens=50000,
        n = 1,
        stop=None,
    )
    summary_text = summary.choices[0].text.strip()
    summaries.append(summary_text)

# Generate a one-pager summarizing the entire repository
one_pager = "\n".join(summaries)
print(one_pager)
