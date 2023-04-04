import openai
import env

# Initialize OpenAI API
openai.api_key = env.API_KEY


def summarize_content(content):
    summary = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant who is also an expert Software Engineer. You will be given some code and are asked to summarize its functionality and significance in the codebase that it comes from in 2 sentences or less."},
            {"role": "user", "content": content},
        ],
    )
    return summary["choices"][0]["message"]
