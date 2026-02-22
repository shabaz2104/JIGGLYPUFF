import os
from dotenv import load_dotenv
# ✅ CHANGE: Import from langfuse.openai instead of openai
from langfuse.openai import AzureOpenAI 

load_dotenv()

# This client now automatically sends trace data to Langfuse
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)

def generate_response(user_input, tool_result, prediction=None):
    try:
        # 🔥 Smalltalk shortcut
        if tool_result.get("status") == "smalltalk":
            return "Hello! How can I assist you with your pharmacy needs today?"

        # 🔒 Prescription enforcement shortcut
        if tool_result.get("reason") == "prescription_required":
            return "This medication requires a valid prescription. Please upload or verify your prescription before placing the order."

        # 🔒 Monthly limit enforcement shortcut
        if tool_result.get("reason") == "monthly_limit_exceeded":
            return (
                f"You have exceeded the allowed monthly limit for this medication. "
                f"The maximum allowed is {tool_result.get('details', {}).get('max_limit')} units per month."
            )

        # ------------------------------
        # Build safe backend summary
        # ------------------------------
        backend_summary = str(tool_result)

        # ------------------------------
        # Inject predictive suggestion
        # ------------------------------
        prediction_text = ""
        if prediction and prediction.get("refill_suggestion"):
            prediction_text = f"""
Additional Context:
The user frequently orders {prediction.get("medicine")}.
You may politely suggest reordering if appropriate.
"""

        # ------------------------------
        # System prompt (SAFE + CLEAR)
        # ------------------------------
        system_prompt = """
You are a professional pharmacy assistant.
Your job:
- Respond clearly and politely.
- Use backend data strictly.
- Do not invent data.
- If order failed, explain clearly.
- If success, confirm clearly.
- If refill opportunity exists, suggest it naturally.
Never mention backend systems.
Never expose internal JSON.
Keep responses user-friendly.
"""

        # ------------------------------
        # Call Azure OpenAI (Tracked by Langfuse)
        # ------------------------------
        response = client.chat.completions.create(
            model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
            # ✅ ADDED: This name appears in your Langfuse dashboard
            name="pharmacy-response-generation", 
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": f"""
User Input:
{user_input}
Backend Result:
{backend_summary}
{prediction_text}
Generate the final response for the user.
"""
                }
            ],
            temperature=0.5,
            max_tokens=400
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error generating response: {str(e)}"
