from agents.core.extractor import extract_order
from agents.core.controller import process_order
from agents.core.responder import generate_response


def run_agent(user_input: str):
    try:
        # Step 1: Extract structured order using GPT
        extracted_order = extract_order(user_input)

        # Step 2: Process order using controller (tools)
        tool_result = process_order(extracted_order)

        # Step 3: Generate final human-friendly response using GPT
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
