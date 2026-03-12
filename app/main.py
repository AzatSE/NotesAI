from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi.middleware.cors import CORSMiddleware
from app.api.main import api_router

def custom_generate_unique_id(route: APIRoute) -> str:
    tag=route.tags[0] if route.tags else "default"
    return f"{tag}-{route.name}"



app = FastAPI(
    generate_unique_id_function=custom_generate_unique_id,
)

origins = [
    "http://localhost:5173",
    "http://localhost",
    "http://127.0.0.1:5173",
    "http://127.0.0.1"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "hello"}


app.include_router(api_router)