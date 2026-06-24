from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str
    recommended_products: list[dict] | None = None