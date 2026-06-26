import requests
from fastapi import FastAPI, HTTPException

from shared.parser import parse_url_and_save
from shared.schemas import ParseRequest

app = FastAPI(title="Parser Service", version="1.0.0")


@app.get("/")
def root():
    return {
        "message": "Parser service is running",
        "docs": "/docs",
        "endpoint": "POST /parse",
    }


@app.post("/parse")
def parse(data: ParseRequest):
    try:
        return parse_url_and_save(str(data.url))
    except requests.RequestException as exc:
        raise HTTPException(status_code=500, detail=f"Request error: {exc}") from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Parser error: {exc}") from exc
