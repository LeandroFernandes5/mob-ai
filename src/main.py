from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.external_integration import fetch_external_data

app = FastAPI(title="AI Platform")

class QueryRequest(BaseModel):
    message: str
    interface_id: str

@app.post("/v1/query")
async def handle_query(request: QueryRequest):
    if not request.interface_id or not request.message:
        raise HTTPException(status_code=400, detail="Both 'interface_id' and 'message' must be provided.")
    context = {
        "interface_id": request.interface_id,
        "model_provider": "openai",
        "question": request.message
    }
    result = fetch_external_data(context)
    if result.startswith("Error:"):
        raise HTTPException(status_code=400, detail=result)
    return {"response": result}
