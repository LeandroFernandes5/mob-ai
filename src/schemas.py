from pydantic import BaseModel
from typing import Optional

class UserQueryRequest(BaseModel):
    interface_id: str
    user_input: str
    user_context: Optional[dict] = None  # Could include user ID, role, session data, etc.

class AIResponse(BaseModel):
    response_text: str
    metadata: Optional[dict] = None