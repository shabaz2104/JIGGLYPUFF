import os
import json
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

client = AzureOpenAI(
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
)

SYSTEM_PROMPT = """
Return JSON:
{
  "intent": "order | inventory | history | update_stock"
}
"""


def classify_intent(user_input: str) -> str:

    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ],
        temperature=0,
        max_tokens=50
    )

    raw_output = response.choices[0].message.content.strip()

    parsed = json.loads(raw_output)

    return parsed["intent"]
