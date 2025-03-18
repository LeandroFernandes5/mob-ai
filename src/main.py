from fastapi import FastAPI, HTTPException
from src.schemas import UserQueryRequest, AIResponse
from src.config_manager import get_configuration
from src.prompt_orchestrator import build_prompt
from src.model_adapter import call_model
from src.response_handler import format_response
from src.external_integration import fetch_external_data

app = FastAPI(title="Generic AI Platform")

@app.get("/")
def health_check():
    return {"status": "OK", "message": "AI Platform is running"}

@app.post("/v1/query", response_model=AIResponse)
def handle_query(request: UserQueryRequest):
    """
    Main endpoint to handle user queries for any use case (interface).
    """
    # 1. Retrieve config for the interface
    try:
        config = get_configuration(request.interface_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Interface configuration not found.")
    
    system_prompt = config["system_prompt"]
    model_id = config["model_id"]
    parameters = config["parameters"]

    # 2. If needed, fetch external data or do any custom steps
    external_data = fetch_external_data(request.user_context or {})

    # 3. Build final prompt
    # Optionally include external data in the prompt if desired
    final_prompt = build_prompt(
        system_prompt=system_prompt,
        user_input=request.user_input + " " + external_data,
        user_context=request.user_context or {}
    )

    # 4. Call the AI model
    raw_model_output = call_model(model_id, final_prompt, parameters)

    # 5. Post-process the response
    final_output = format_response(raw_model_output)

    # 6. Return the response
    return AIResponse(response_text=final_output, metadata={"model_id": model_id})