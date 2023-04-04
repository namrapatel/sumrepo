import openai
import env

# Initialize OpenAI API
openai.api_key = env.API_KEY

prompts_string = """You are a helpful assistant who is also an expert Software Engineer. 
You will be given the name of a file, the file path to that file, and the code that is within the file,
and your job is to determine what the functionality of the code in the file is in the contex of the entire codebase
that the project comes from and summarize the functionality and purpose of the code in the file in 3 sentences or less.
"""

def summarize_content(content):
    summary = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompts_string},
            {"role": "user", "content": content},
        ],
    )
    return summary["choices"][0]["message"]
