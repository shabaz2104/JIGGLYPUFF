# agents/core/extractor.py

import os
import json
from dotenv import load_dotenv
from openai import AzureOpenAI
from pydantic import BaseModel
from typing import Optional

load_dotenv()


class StructuredRequest(BaseModel):
    intent: Optional[str] = "smalltalk"
    medicine_name: Optional[str] = None
    quantity: Optional[int] = None
    delta: Optional[int] = None
    customer_id: Optional[str] = None


client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)


def extract_structured_request(user_input: str):

    system_prompt = """
You are a pharmacy intent extraction engine.

Return ONLY JSON in this format:

{
  "intent": "order | inventory | history | update_stock | smalltalk",
  "medicine_name": string or null,
  "quantity": integer or null,
  "delta": integer or null,
  "customer_id": string or null
}

If user message is casual greeting or unrelated,
set intent to "smalltalk".

Rules:
- order requires medicine_name + quantity
- inventory requires medicine_name
- history requires no medicine
- update_stock requires medicine_name + delta
- If not provided, use null
Return only JSON.
"""

    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        temperature=0
    )

    parsed = json.loads(response.choices[0].message.content.strip())

    return StructuredRequest(**parsed)