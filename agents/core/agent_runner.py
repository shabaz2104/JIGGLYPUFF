# agents/core/agent_runner.py

from agents.core.extractor import extract_structured_request
from agents.core.controller import handle_intent
from agents.core.responder import generate_response
from agents.core.predictor import analyze_refill_opportunity
from agents.core.tracing import langfuse 

def run_agent(user_input: str):
    try:
        # 1. Pre-extract or define the customer ID (e.g., from your auth session)
        # For now, we'll use a placeholder or extract it first
        customer_id = "PAT001" 

        # ✅ ADDED: 'user_id' parameter
        # This links the entire trace to this specific customer in Langfuse
        with langfuse.start_as_current_observation(
            name="pharmacy-agent-run",
            input={"user_input": user_input},
            user_id=customer_id  # 👈 This enables per-user analytics!
        ) as trace:

            # -------------------------------
            # Intent Extraction
            # -------------------------------
            with langfuse.start_as_current_observation(name="intent_extraction") as span:
                structured = extract_structured_request(user_input)
                span.update(output=structured.model_dump())
            
            # Update customer_id if the extractor found a real one
            if structured.customer_id:
                customer_id = structured.customer_id
                # Update the trace metadata if it changed
                trace.update(user_id=customer_id)

            # -------------------------------
            # Backend Handling
            # -------------------------------
            with langfuse.start_as_current_observation(name="controller_execution") as span:
                backend_result = handle_intent(structured)
                span.update(output=backend_result)

            # -------------------------------
            # Predictive Intelligence
            # -------------------------------
            with langfuse.start_as_current_observation(name="predictive_intelligence") as span:
                prediction = analyze_refill_opportunity(customer_id)
                span.update(output=prediction)

            # -------------------------------
            # Final Response Generation (Azure GPT-4o)
            # -------------------------------
            # This call inside generate_response now automatically 
            # inherits the user_id and trace context!
            final_response = generate_response(
                user_input,
                backend_result,
                prediction
            )

            trace.update(output={"response": final_response})

            return {
                "status": "success",
                "response": final_response
            }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
    finally:
        langfuse.flush()
