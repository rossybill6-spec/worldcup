from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

def setup_cors(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://localhost:5173", "http://localhost:8000", "https://worldcup-orcin-chi.vercel.app", "*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
