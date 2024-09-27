import sys

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

sys.path.append(".")

from src.graph import Workflow
from src.utils import database

app = FastAPI()
workflow_app = Workflow().app
database.init_db()


class ChatHistory(BaseModel):
    query: str = Field(
        ...,
        title="Query",
        description="User query",
        examples=["What was my last transaction?"],
    )
    response: str = Field(
        ...,
        title="Response",
        description="Agent response",
        examples=["Your last transaction was $100 to Amazon."],
    )
    agent: str = Field(
        ...,
        title="Agent",
        description="Agent name",
        examples=["transaction-expert"],
    )
    timestamp: str = Field(
        ...,
        title="Timestamp",
        description="Timestamp of the chat",
        examples=["2021-08-01 12:00:00"],
    )


class LoginRequest(BaseModel):
    user_id: int


@app.post("/login", response_model=list[ChatHistory])
async def handle_login(request: LoginRequest) -> list[dict[str, str]]:
    user_id = request.user_id
    chat_history = database.get_chat_history(user_id)
    return chat_history


class QueryRequest(BaseModel):
    query: str
    user_id: int


@app.post("/query", response_model=str)
async def handle_query(request: QueryRequest) -> str:
    user_id = request.user_id
    query = request.query

    chat_history = database.get_chat_history(user_id)
    parsed_chat_history = ""
    for i, history in enumerate(chat_history):
        parsed_chat_history += f"{i+1}. User: {history['query']}\nAgent ({history['agent']}): {history['response']}\n"

    state = {
        "query": query,
        "user_id": user_id,
        "chat_history": parsed_chat_history,
    }

    try:
        response = workflow_app.invoke(state)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    agent_output = response["agent_output"]
    database.add_chat_history(
        user_id, query, agent_output["output"], agent_output["agent"]
    )

    return agent_output["output"]


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
