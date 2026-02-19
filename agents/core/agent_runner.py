from agents.core.extractor import extract_structured_data
from agents.core.controller import handle_intent
from agents.core.responder import generate_response


def run_agent(user_input: str):
    try:
        # STEP 1 — Extract structured data (intent + entities)
        structured_data = extract_structured_data(user_input)

        # If extraction itself failed
        if isinstance(structured_data, dict) and structured_data.get("status") == "error":
            return structured_data

        # STEP 2 — Execute logic based on intent
        tool_result = handle_intent(structured_data)

        # STEP 3 — Generate final GPT response
        final_message = generate_response(user_input, tool_result)

        return {
            "status": "success",
            "response": final_message
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
