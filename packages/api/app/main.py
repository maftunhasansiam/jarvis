from fastapi import FastAPI
from packages.api.app.routes import agent

app = FastAPI(title="Jarvis - Agent API (M1)")

app.include_router(agent.router, prefix="/v1/agent", tags=["agent"])


@app.get("/")
def read_root():
    return {"msg": "Jarvis Agent API (M1) - healthy"}
