import os
import json
from dotenv import load_dotenv
from openai import AzureOpenAI
from agents.models.schemas import MedicineOrder

load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)


def extract_structured_data(user_input: str):

    system_prompt = """
You are a structured data extraction system for a pharmacy AI.

Your job is to classify the intent and extract relevant data.

Possible intents:
- order
- inventory
- history
- update_stock

Return ONLY valid JSON in this format:

{
  "intent": "one_of_the_above",
  "medicine_name": string or null,
  "quantity": integer or null,
  "stock": integer or null,
  "customer_id": string or null
}

Rules:
- Do NOT include explanations.
- Do NOT include markdown.
- Return JSON only.
"""

    try:
        response = client.chat.completions.create(
            model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=0
        )

        raw_output = response.choices[0].message.content.strip()

        parsed = json.loads(raw_output)

        return MedicineOrder(**parsed)

    except Exception as e:
        raise Exception(f"Extraction failed: {str(e)}")
