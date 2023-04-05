import openai
import env

# Initialize OpenAI API
openai.api_key = env.API_KEY

file_summary_prompt = """You are a helpful assistant who is also an expert Software Engineer. 
You will be given the name of a file, the file path to that file, and the code that is within the file,
and your job is to determine what the functionality of the code in the file is in the contex of the entire codebase
that the project comes from and summarize the functionality and purpose of the code in the file in 3 sentences or less.
"""

def summarize_file(content):
    print("Summarizing content...\n ")
    summary = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": file_summary_prompt},
            {"role": "user", "content": content},
        ],
    )

    return summary["choices"][0]["message"]

summary_prompt = """You are a helpful assistant who is also an expert Software Engineer.
You will be given a list of summarize that describe the functionality of the code in each file in the project, 
alongside the name of the file and the file path to that file, and your job is to write a summary of the project that describes 
(1) the overall functionality and architecture of the project as an overview, (2) each component of the project (highlighted with a header) and 
(3) any sub-components of each component that may be worth mentioning briefly. Do not copy and paste the summaries of each file, and do not simply describe
what each file does in a list. Instead, write a summary that describes the overall functionality of the project and the functionality of each major component of the project.
The writing should resemble a technical blog post or a technical documentation page.
"""

def summarize_summaries(summaries):
    print("Summarizing summaries...\n ")
    summary = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": summary_prompt},
            {"role": "user", "content": summaries},
        ],
    )

    return summary["choices"][0]["message"]