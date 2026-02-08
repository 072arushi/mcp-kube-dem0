from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import os

app = FastAPI()

class Tool(BaseModel):
    name: str
    description: str
    input_schema: dict

@app.get("/tools")
def list_tools():
    return [
        Tool(
            name="get_time",
            description="Get the current server time",
            input_schema={}
        ),
        Tool(
            name="get_cluster_name",
            description="Return the Kubernetes cluster name",
            input_schema={}
        ),
    ]

@app.post("/tools/get_time")
def get_time():
    return {"time": datetime.utcnow().isoformat()}

@app.post("/tools/get_cluster_name")
def get_cluster_name():
    return {"cluster": os.getenv("CLUSTER_NAME", "unknown")}
