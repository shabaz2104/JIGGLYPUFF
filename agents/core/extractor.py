# agents/core/extractor.py

import os
import json
from dotenv import load_dotenv
from openai import AzureOpenAI
from pydantic import BaseModel
from typing import Optional

load_dotenv()


# ==========================
# Structured Request Schema
# ==========================
class StructuredRequest(BaseModel):
    intent: Optional[str] = "smalltalk"
    medicine_name: Optional[str] = None
    quantity: Optional[int] = None
    delta: Optional[int] = None
    customer_id: Optional[str] = None


# ==========================
# Azure OpenAI Client
# ==========================
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)


# ==========================
# Extraction Function
# ==========================
def extract_structured_request(user_input: str) -> StructuredRequest:

    system_prompt = """
You are a pharmacy intent extraction engine.

Return ONLY valid JSON in this format:

{
  "intent": "order | inventory | history | update_stock | upload_prescription | smalltalk",
  "medicine_name": string or null,
  "quantity": integer or null,
  "delta": integer or null,
  "customer_id": string or null
}

Intent Rules:

- order → requires medicine_name + quantity
- inventory → requires medicine_name
- history → no medicine required
- update_stock → requires medicine_name + delta
- upload_prescription → requires medicine_name
- casual greetings → smalltalk

Examples:
"I want 2 Paracetamol" → order
"Is Amoxicillin available?" → inventory
"I uploaded prescription for Amoxicillin" → upload_prescription
"Hi" → smalltalk

If a field is missing, set it to null.

Return ONLY JSON.
"""

    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        temperature=0
    )

    raw_output = response.choices[0].message.content.strip()

    try:
        parsed = json.loads(raw_output)
        return StructuredRequest(**parsed)
    except Exception:
        raise ValueError(f"Invalid model output: {raw_output}")