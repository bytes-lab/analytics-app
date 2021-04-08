import traceback

from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

from utils import *


app = FastAPI()


class RunRequest(BaseModel):
    token: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None


@app.get("/")
def index():
    return "Service is ready."


@app.post("/compute")
async def compute(run: RunRequest):
    resp = {
        'tenants': get_tenants(),
        'resource_types': get_resource_types(),
        'breakdown_resource_type': get_breakdown_resource_type(run.start_date, run.end_date),
        'breakdown_client': get_breakdown_client(run.start_date, run.end_date),
        'breakdown_time': get_breakdown_time(run.start_date, run.end_date),
        'breakdown_resource_tier': get_breakdown_resource_tier(run.start_date, run.end_date),
    }

    return resp
