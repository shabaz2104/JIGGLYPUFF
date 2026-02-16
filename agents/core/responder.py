import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)

def generate_response(user_input, tool_result):
    try:
        response = client.chat.completions.create(
            model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional pharmacy assistant. Generate a clear, concise, and friendly response based on the tool result."
                },
                {
                    "role": "user",
                    "content": f"""
User Request:
{user_input}

Tool Result:
{tool_result}

Generate the final response to the user.
"""
                }
            ],
            temperature=0.5,
            max_tokens=300
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error generating response: {str(e)}"
