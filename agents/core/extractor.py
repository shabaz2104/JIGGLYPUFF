import os
import json
from openai import AzureOpenAI
from dotenv import load_dotenv
from agents.models.schemas import MedicineOrder

# Load .env from project root
load_dotenv()

# Initialize Azure client
client = AzureOpenAI(
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
)


def extract_order(user_message: str) -> MedicineOrder:
    system_prompt = """
You are a strict medical order extraction engine.

Convert user message into JSON matching this schema:

{
  "intent": "order | availability_check | refill | general_query",
  "medicine_name": "string",
  "dosage": "string or null",
  "quantity": integer
}

Rules:
- Return ONLY valid JSON.
- No explanations.
- No extra text.
- If missing dosage, set null.
- If quantity not specified, default to 1.
"""

    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        temperature=0,
    )

    raw_output = response.choices[0].message.content

    try:
        parsed = json.loads(raw_output)
        return MedicineOrder(**parsed)
    except Exception:
        raise ValueError(f"Invalid model output: {raw_output}")
