from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from api.task import tasks_api

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8001",
    "http://frontend",
    "http://frontend:8001",
    "http://127.0.0.1"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tasks_api, prefix='/tasks', tags=['tasks'])
