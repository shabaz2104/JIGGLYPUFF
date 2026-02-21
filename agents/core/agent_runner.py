# agents/core/agent_runner.py

from agents.core.extractor import extract_structured_request
from agents.core.controller import handle_intent
from agents.core.responder import generate_response
from agents.core.predictor import analyze_refill_opportunity
from agents.core.tracing import langfuse  # 🔥 added


def run_agent(user_input: str):

    try:

        # -------------------------------
        # 🔍 Start Langfuse Trace
        # -------------------------------
        trace = langfuse.start_trace(
            name="pharmacy-agent-run",
            input={"user_input": user_input}
        )

        structured = extract_structured_request(user_input)

        trace.log(
            name="extraction",
            output=structured.model_dump()
        )

        backend_result = handle_intent(structured)

        trace.log(
            name="backend_result",
            output=backend_result
        )

        # -------------------------------
        # 🔮 Predictive Intelligence Layer
        # -------------------------------
        customer_id = structured.customer_id or "PAT001"
        prediction = analyze_refill_opportunity(customer_id)

        trace.log(
            name="prediction",
            output=prediction
        )

        # Pass prediction into responder
        final_response = generate_response(
            user_input,
            backend_result,
            prediction
        )

        trace.log(
            name="final_response",
            output={"response": final_response}
        )

        trace.end()

        return {
            "status": "success",
            "response": final_response
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }