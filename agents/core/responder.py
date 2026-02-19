import os
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)


def generate_response(user_input, tool_result):

    system_prompt = """
You are a pharmacy system response generator.

Your job is to convert structured backend results into a clean, professional message.

DO NOT invent information.
DO NOT create fake order IDs.
ONLY use the data present inside tool_result.
Be concise and factual.
"""

    try:
        response = client.chat.completions.create(
            model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": f"""
User input:
{user_input}

Backend result:
{tool_result}

Generate a final response.
"""
                }
            ],
            temperature=0,
            max_tokens=200
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Error generating response: {str(e)}"
