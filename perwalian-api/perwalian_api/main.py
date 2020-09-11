from typing import Optional
import os
import sys

from starlette.responses import JSONResponse

from perwalian_api.store import store
from perwalian_api.model import Mahasiswa

from fastapi import FastAPI, Response, status
import uvicorn

app = FastAPI()


@app.post("/mahasiswa")
def post_mahasiswa(mahasisa: Mahasiswa):
    store.create(mahasisa)
    return Response(status_code=status.HTTP_201_CREATED)


@app.get("/mahasiswa/{id}")
def get_mahasiswa(id: str):
    item = store.get(Mahasiswa, id)

    if item == None:
        return JSONResponse({}, status.HTTP_404_NOT_FOUND)

    return item


@app.post("/store/_clear")
def route_store_clear():
    store.clear()
    return "ok"