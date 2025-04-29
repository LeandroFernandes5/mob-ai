from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

from src.external_integration import fetch_external_data
from src.config_manager import ConfigManager

app = FastAPI(title="AI Platform")

class QueryRequest(BaseModel):
    message: str
    interface_id: str
    model_provider: Optional[str] = None  # Optional field for explicit model selection

@app.post("/v1/query")
async def handle_query(request: QueryRequest):
    if not request.interface_id or not request.message:
        raise HTTPException(status_code=400, detail="Both 'interface_id' and 'message' must be provided.")
    
    # Get interface configuration
    config_manager = ConfigManager()
    try:
        interface_config = config_manager.get_configuration(request.interface_id)
    except KeyError:
        raise HTTPException(status_code=400, detail=f"No configuration found for interface: {request.interface_id}")
    
    # If model_provider is not specified, use the first available provider from config
    model_provider = request.model_provider
    if not model_provider:
        available_providers = list(interface_config.get('model_providers', {}).keys())
        if not available_providers:
            raise HTTPException(status_code=400, detail=f"No model providers configured for interface: {request.interface_id}")
        model_provider = available_providers[0]
    
    # Prepare context for external integration
    context = {
        "interface_id": request.interface_id,
        "model_provider": model_provider,
        "question": request.message
    }
    
    result = fetch_external_data(context)
    if result.startswith("Error:"):
        raise HTTPException(status_code=400, detail=result)
    return {"response": result}
